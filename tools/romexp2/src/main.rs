extern crate clap;
extern crate memmap;
extern crate glfw;
extern crate gl;

use clap::{Arg,App};

use memmap::{Mmap, Protection};

use glfw::{Action, Context, Key};
use gl::types::*;
use std::mem;
use std::ptr;
use std::str;
use std::ffi::CString;


// Vertex data
static VERTEX_DATA: [GLfloat; 12] = [
    -1.0, 1.0, -1.0, -1.0, 1.0, -1.0,
    -1.0, 1.0, 1.0, 1.0, 1.0, -1.0,
];

// Shader sources
static VS_SRC: &'static str = include_str!("vs.glsl");

static FS_SRC: &'static str = include_str!("fs.glsl");

fn compile_shader(src: &str, ty: GLenum) -> GLuint {
    let shader;
    unsafe {
        shader = gl::CreateShader(ty);
        // Attempt to compile the shader
        let c_str = CString::new(src.as_bytes()).unwrap();
        gl::ShaderSource(shader, 1, &c_str.as_ptr(), ptr::null());
        gl::CompileShader(shader);

        // Get the compile status
        let mut status = gl::FALSE as GLint;
        gl::GetShaderiv(shader, gl::COMPILE_STATUS, &mut status);

        // Fail on error
        if status != (gl::TRUE as GLint) {
            let mut len = 0;
            gl::GetShaderiv(shader, gl::INFO_LOG_LENGTH, &mut len);
            let mut buf = Vec::with_capacity(len as usize);
            buf.set_len((len as usize) - 1); // subtract 1 to skip the trailing null character
            gl::GetShaderInfoLog(shader,
                                 len,
                                 ptr::null_mut(),
                                 buf.as_mut_ptr() as *mut GLchar);
            panic!("{}",
                   str::from_utf8(&buf)
                       .ok()
                       .expect("ShaderInfoLog not valid utf8"));
        }
    }
    shader
}

fn link_program(vs: GLuint, fs: GLuint) -> GLuint {
    unsafe {
        let program = gl::CreateProgram();
        gl::AttachShader(program, vs);
        gl::AttachShader(program, fs);
        gl::LinkProgram(program);
        // Get the link status
        let mut status = gl::FALSE as GLint;
        gl::GetProgramiv(program, gl::LINK_STATUS, &mut status);

        // Fail on error
        if status != (gl::TRUE as GLint) {
            let mut len: GLint = 0;
            gl::GetProgramiv(program, gl::INFO_LOG_LENGTH, &mut len);
            let mut buf = Vec::with_capacity(len as usize);
            buf.set_len((len as usize) - 1); // subtract 1 to skip the trailing null character
            gl::GetProgramInfoLog(program,
                                  len,
                                  ptr::null_mut(),
                                  buf.as_mut_ptr() as *mut GLchar);
            panic!("{}",
                   str::from_utf8(&buf)
                       .ok()
                       .expect("ProgramInfoLog not valid utf8"));
        }
        program
    }
}

struct Visualizer {
    glfw : glfw::Glfw,
    win : glfw::Window,
    events : std::sync::mpsc::Receiver<(f64, glfw::WindowEvent)>,
    program : GLuint,
}

impl Visualizer {
    fn new(size : (u32, u32), data_sz : usize) -> Visualizer {
        let mut glfw = glfw::init(glfw::FAIL_ON_ERRORS).unwrap();
        let (mut window, events) = glfw.create_window(size.0, size.1 ,
                                                      "ROM explorer",
                                                      glfw::WindowMode::Windowed)
            .expect("Failed to create GLFW window.");
        window.set_key_polling(true);
        window.make_current();
        gl::load_with(|name| window.get_proc_address(name) as *const _);
        // Create vertex shader
        let vs = compile_shader(VS_SRC, gl::VERTEX_SHADER);
        // Fragment shader needs size of data at compile time (in uints)
        let fsstr = String::from(FS_SRC).replace("{}",(data_sz/4).to_string().as_str());
        let fs = compile_shader(fsstr.as_str(), gl::FRAGMENT_SHADER);
        let program = link_program(vs, fs);

        let mut vao = 0; let mut vbo = 0;
        unsafe {
        // Create Vertex Array Object
            gl::GenVertexArrays(1, &mut vao);
            gl::BindVertexArray(vao);
            // Create a Vertex Buffer Object and copy the vertex data to it
            gl::GenBuffers(1, &mut vbo);
            gl::BindBuffer(gl::ARRAY_BUFFER, vbo);
            gl::BufferData(gl::ARRAY_BUFFER,
                           (VERTEX_DATA.len() * mem::size_of::<GLfloat>()) as GLsizeiptr,
                           mem::transmute(&VERTEX_DATA[0]),
                           gl::STATIC_DRAW);
            // Use shader program
            gl::UseProgram(program);
            gl::BindFragDataLocation(program, 0, CString::new("out_color").unwrap().as_ptr());
            // Specify the layout of the vertex data
            let pos_attr = gl::GetAttribLocation(program, CString::new("position").unwrap().as_ptr());
            gl::EnableVertexAttribArray(pos_attr as GLuint);
            gl::VertexAttribPointer(pos_attr as GLuint,
                                    2,
                                    gl::FLOAT,
                                    gl::FALSE as GLboolean,
                                    0,
                                    ptr::null());
        }
        let vz = Visualizer { glfw : glfw, win : window, events: events, program : program };
        vz.set_size(size);
        vz
    }

    fn set_data(&self, dat : *const GLuint, len : usize) {
        unsafe { 
            let texloc = gl::GetUniformLocation(self.program,CString::new("rom").unwrap().as_ptr());
            gl::Uniform1uiv(texloc,(len/4) as i32,dat);
        }
    }

    fn set_size(&self, size : (u32, u32)) {
        unsafe {
            gl::Uniform1ui(
                gl::GetUniformLocation(self.program,CString::new("ww").unwrap().as_ptr()),
                size.0);
            gl::Uniform1ui(
                gl::GetUniformLocation(self.program,CString::new("wh").unwrap().as_ptr()),
                size.1);
        }
    }

    fn set_stride(&self, stride : u32) {
        unsafe {
            gl::Uniform1ui(
                gl::GetUniformLocation(self.program,CString::new("stride").unwrap().as_ptr()),
                stride);
        }
    }
}

        

fn main() {
    let matches = App::new("ROM image explorer")
        .version("0.1")
        .author("phooky@gmail.com")
        .about("Quickly analyze ROM dumps and other binary blobs")
        .arg(Arg::with_name("ROM")
            .help("ROM file to analyze")
            .required(true))
        .get_matches();

    let rom_path = matches.value_of("ROM").unwrap();
    let rom = match Mmap::open_path(rom_path,Protection::Read) {
        Ok(r) => r,
        Err(e) => { println!("Could not open {}: {}",rom_path,e); return; },
    };
    
    println!("Opened {}; size {} bytes",rom_path,rom.len());

    let mut viz = Visualizer::new((512, 512), rom.len());
    viz.set_data(rom.ptr() as *const GLuint, rom.len());
    viz.set_stride(8);
    
    while !viz.win.should_close() {
        unsafe { gl::ClearColor(1.0,0.0,0.0,1.0) };
        unsafe { gl::Clear(gl::COLOR_BUFFER_BIT) };
        unsafe { gl::DrawArrays(gl::TRIANGLES, 0, 6) };
        viz.win.swap_buffers();
        viz.glfw.poll_events();
        for (_, event) in glfw::flush_messages(&viz.events) {
            println!("EVT: {:?}", event);
            match event {
                glfw::WindowEvent::Key(Key::Escape, _, Action::Press, _) => {
                    viz.win.set_should_close(true)
                },
                _ => {},
            }
        }
    }

}

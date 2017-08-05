extern crate clap;
extern crate memmap;
extern crate glfw;
extern crate gl;

use clap::{Arg,App};

use memmap::{Mmap, Protection};

use glfw::{Action, Context, Key};

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

    let mut glfw = glfw::init(glfw::FAIL_ON_ERRORS).unwrap();
    let (mut window, events) = glfw.create_window(300,300,"ROM explorer", glfw::WindowMode::Windowed)
        .expect("Failed to create GLFW window.");
    window.set_key_polling(true);
    window.make_current();
    gl::load_with(|name| window.get_proc_address(name) as *const _);
    while !window.should_close() {
        unsafe { gl::ClearColor(1.0,0.0,0.0,1.0) };
        unsafe { gl::Clear(gl::COLOR_BUFFER_BIT) };
        window.swap_buffers();
        glfw.poll_events();
        for (_, event) in glfw::flush_messages(&events) {
            println!("EVT: {:?}", event);
            match event {
                glfw::WindowEvent::Key(Key::Escape, _, Action::Press, _) => {
                    window.set_should_close(true)
                },
                _ => {},
            }
        }
    }

}

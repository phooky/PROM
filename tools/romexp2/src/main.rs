extern crate gtk;
extern crate clap;
extern crate memmap;

use clap::{Arg,App};

use gtk::prelude::*;
use gtk::{Button, GLArea, Window, Box, WindowType};

use memmap::{Mmap, Protection};

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

    if gtk::init().is_err() {
        println!("Failed to initialize GTK.");
        return;
    }

    let window = Window::new(WindowType::Toplevel);
    window.set_title("First GTK+ Program");
    window.set_default_size(350, 70);
    let gbox = Box::new(gtk::Orientation::Vertical, 2);
    let area = GLArea::new();
    area.set_size_request(350,200);
    gbox.add(&area);
    let button = Button::new_with_label("Click me!");
    gbox.add(&button);
    window.add(&gbox);
    window.show_all();

    area.connect_render(|_, context| {
        println!("Render");
        Inhibit(false)
    });

    window.connect_delete_event(|_, _| {
        gtk::main_quit();
        Inhibit(false)
    });

    button.connect_clicked(|_| {
        println!("Clicked!");
    });

    gtk::main();
    println!("Hello, world!");
}

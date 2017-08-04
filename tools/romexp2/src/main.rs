extern crate gtk;
extern crate clap;

use clap::{Arg,App};

use gtk::prelude::*;
use gtk::{Button, Window, WindowType};

fn main() {
    let matches = App::new("ROM image explorer")
        .version("0.1")
        .author("phooky@gmail.com")
        .about("Quickly analyze ROM dumps and other binary blobs")
        .arg(Arg::with_name("ROM")
            .help("ROM file to analyze")
            .required(true))
        .get_matches();

    if gtk::init().is_err() {
        println!("Failed to initialize GTK.");
        return;
    }

    let window = Window::new(WindowType::Toplevel);
    window.set_title("First GTK+ Program");
    window.set_default_size(350, 70);
    let button = Button::new_with_label("Click me!");
    window.add(&button);
    window.show_all();

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

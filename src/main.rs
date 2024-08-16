mod bandcamp;

use clap::{Arg, Command};

fn main() {
    let matches = Command::new("DL Tool")
        .version("1.0")
        .about("A tool to download media from various platforms")
        .subcommand(
            Command::new("all")
                .about("Download all artist's albums that the user has followed")
                .arg(Arg::new("username")
                    .help("The username of the user")
                    .required(true))
                .arg(Arg::new("multi_thread")
                    .help("Use multi-threading")
                    .long("multi_thread")))
        .subcommand(
            Command::new("artist")
                .about("Download all albums of a specific artist")
                .arg(Arg::new("artist_url")
                    .help("The URL of the artist")
                    .required(true)))
        .subcommand(
            Command::new("album")
                .about("Download a single album")
                .arg(Arg::new("album_url")
                    .help("The URL of the album")
                    .required(true)))
        .get_matches();

    match matches.subcommand() {
        Some(("all", sub_m)) => {
            let username = sub_m.get_one::<String>("username").unwrap();
            let multi_thread = sub_m.contains_id("multi_thread");
            bandcamp::download_all_followed(username, multi_thread);
        }
        Some(("artist", sub_m)) => {
            let artist_url = sub_m.get_one::<String>("artist_url").unwrap();
            bandcamp::download_artist_albums(&artist_url, 1, false);
        }
        Some(("album", sub_m)) => {
            let album_url = sub_m.get_one::<String>("album_url").unwrap();
            bandcamp::download_album(&album_url, 1, 1);
        }
        _ => println!("Invalid command"),
    }
}

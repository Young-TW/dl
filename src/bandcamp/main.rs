use reqwest;
use scraper::{Html, Selector};
use std::process::Command;

fn get_artist_albums(artist_url: &str) -> Vec<String> {
    let res = reqwest::blocking::get(artist_url).unwrap();
    let body = res.text().unwrap();
    let document = Html::parse_document(&body);
    let selector = Selector::parse("a.music-grid-item").unwrap();

    let mut album_links = Vec::new();

    for element in document.select(&selector) {
        if let Some(album_url) = element.value().attr("href") {
            // 檢查URL是否是完整的，如果不是就補上藝術家主頁的前綴
            let full_url = if album_url.starts_with("http") {
                album_url.to_string()
            } else {
                format!("{}{}", artist_url, album_url)
            };
            album_links.push(full_url);
        }
    }

    album_links
}

fn download_album(album_url: &str) {
    let output = Command::new("bandcamp-dl")
        .arg(album_url)
        .output()
        .expect("Failed to execute bandcamp-dl");

    if !output.status.success() {
        eprintln!(
            "Failed to download album: {}",
            String::from_utf8_lossy(&output.stderr)
        );
    }
}

fn main() {
    let artist_url = "https://hitnex.bandcamp.com";

    let album_links = get_artist_albums(artist_url);

    for album in album_links {
        download_album(&album);
    }
}

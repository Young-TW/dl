use reqwest::blocking::Client;
use scraper::{Html, Selector};
use std::fs;
use std::process::{Command, Stdio};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

pub fn download_all_followed(username: &str, use_multi_thread: bool) {
    let user_url = format!("https://bandcamp.com/{}/following", username);
    let artist_links = get_followed_artists(&user_url);

    let _total_albums: usize = artist_links
        .iter()
        .map(|link| get_artist_albums(link).len())
        .sum();

    let mut current_count = 1;

    for artist_link in artist_links {
        download_artist_albums(&artist_link, current_count, use_multi_thread);
        current_count += get_artist_albums(&artist_link).len();
    }
}

pub fn download_artist_albums(artist_url: &str, start_count: usize, use_multi_thread: bool) {
    let album_links = get_artist_albums(artist_url);
    let total_albums = album_links.len();
    let current_count = Arc::new(Mutex::new(start_count));

    if use_multi_thread {
        let mut handles = vec![];

        for album_link in album_links {
            let current_count = Arc::clone(&current_count);
            let album_link = album_link.clone();

            let handle = thread::spawn(move || {
                let mut count = current_count.lock().unwrap();
                *count += 1;
                download_album(&album_link, total_albums, *count);
            });

            handles.push(handle);
        }

        for handle in handles {
            let _ = handle.join();
        }
    } else {
        for album_link in album_links {
            let mut count = current_count.lock().unwrap();
            *count += 1;
            download_album(&album_link, total_albums, *count);
        }
    }
}

pub fn download_album(album_url: &str, total_albums: usize, current_count: usize) {
    let album_name = album_url.split('/').last().unwrap_or("unknown");

    if fs::metadata(album_name).is_ok() {
        println!(
            "{}/{} - Album {} already downloaded. Skipping...",
            current_count, total_albums, album_name
        );
        return;
    }

    println!("{}/{} - Downloading {}...", current_count, total_albums, album_name);
    let command = Command::new("bandcamp-dl")
        .arg(album_url)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status();

    match command {
        Ok(status) if status.success() => {
            println!("{}/{} - Download {}: success", current_count, total_albums, album_name);
        }
        _ => {
            println!("{}/{} - Download {}: failed", current_count, total_albums, album_name);
        }
    }
}

fn send_request_with_retry(url: &str, max_retries: u8) -> Option<String> {
    let client = Client::new();
    let mut retries = 0;

    while retries < max_retries {
        let response = client.get(url).send();

        match response {
            Ok(resp) => {
                if resp.status().as_u16() == 429 {
                    retries += 1;
                    println!(
                        "Received 429 Too Many Requests. Retrying in 10 seconds... (Attempt {}/{})",
                        retries, max_retries
                    );
                    thread::sleep(Duration::from_secs(10));
                } else {
                    return resp.text().ok();
                }
            }
            Err(_) => {
                retries += 1;
                println!("Request failed. Retrying... (Attempt {}/{})", retries, max_retries);
            }
        }
    }

    println!("Max retries reached for URL: {}.", url);
    None
}

fn get_followed_artists(user_url: &str) -> Vec<String> {
    println!("Fetching followed artists from {}...", user_url);
    if let Some(html) = send_request_with_retry(user_url, 3) {
        let document = Html::parse_document(&html);
        let selector = Selector::parse("div.fan-image a").unwrap();

        return document
            .select(&selector)
            .filter_map(|element| element.value().attr("href").map(String::from))
            .collect();
    }
    Vec::new()
}

fn get_artist_albums(artist_url: &str) -> Vec<String> {
    if let Some(html) = send_request_with_retry(artist_url, 3) {
        let document = Html::parse_document(&html);
        let selector = Selector::parse("a").unwrap();

        return document
            .select(&selector)
            .filter_map(|element| {
                let href = element.value().attr("href")?;
                if href.starts_with("/track/") || href.starts_with("/album/") {
                    Some(format!("{}{}", artist_url, href))
                } else {
                    None
                }
            })
            .collect();
    }
    Vec::new()
}

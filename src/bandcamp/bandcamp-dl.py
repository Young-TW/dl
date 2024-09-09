import requests
from bs4 import BeautifulSoup
import os
import argparse
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_followed_artists(user_url):
    print(f"Fetching followed artists from {user_url}...")
    response = send_request_with_retry(user_url)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        artist_links = []
        for link in soup.find_all('div', class_='fan-image'):
            a_tag = link.find('a', href=True)
            if a_tag:
                artist_url = a_tag['href']
                artist_links.append(artist_url)
        return artist_links
    else:
        print(f"Failed to fetch followed artists. Status code: {response.status_code if response else 'N/A'}")
        return []

def get_artist_albums(artist_url):
    response = send_request_with_retry(artist_url)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        album_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href.startswith('/track/') or href.startswith('/album/'):
                album_url = artist_url + href
                album_links.append(album_url)
        return album_links
    else:
        print(f"Failed to fetch albums from {artist_url}. Status code: {response.status_code if response else 'N/A'}")
        return []

def send_request_with_retry(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        response = requests.get(url)
        if response.status_code == 429:
            retries += 1
            print(f"Received 429 Too Many Requests. Retrying in 10 seconds... (Attempt {retries}/{max_retries})")
            time.sleep(10)
        else:
            return response
    print(f"Max retries reached for URL: {url}.")
    return None

def download_album(album_url, total_albums, current_count):
    album_name = album_url.split('/')[-1]
    if os.path.exists(album_name):
        print(f"{current_count}/{total_albums} - Album {album_name} already downloaded. Skipping...")
        return

    command = f"bandcamp-dl \"{album_url}\""
    print(f"{current_count}/{total_albums} - Downloading {album_name}...")

    # 隱藏原始輸出
    result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if result.returncode == 0:
        print(f"{current_count}/{total_albums} - Download {album_name}: success")
    else:
        print(f"{current_count}/{total_albums} - Download {album_name}: failed")

def download_artist_albums(artist_url, total_albums, start_count, use_multi_thread):
    album_links = get_artist_albums(artist_url)

    if use_multi_thread:
        with ThreadPoolExecutor() as executor:
            futures = []
            for idx, album_link in enumerate(album_links, start=start_count):
                futures.append(executor.submit(download_album, album_link, total_albums, idx))
            for future in as_completed(futures):
                future.result()
    else:
        for idx, album_link in enumerate(album_links, start=start_count):
            download_album(album_link, total_albums, idx)

def main():
    parser = argparse.ArgumentParser(description='Download albums from Bandcamp.')
    parser.add_argument('mode', choices=['all', 'artist', 'album'], help='Select download mode: "all" for all followed artists, "artist" for a single artist, "album" for a single album.')
    parser.add_argument('--username', type=str, help='The Bandcamp username (required if mode is "all")')
    parser.add_argument('--artist_url', type=str, help='The URL of the artist page (required if mode is "artist" or "album")')
    parser.add_argument('--album_url', type=str, help='The URL of the album page (required if mode is "album")')
    parser.add_argument('--multi_thread', action='store_true', help='Enable multi-threading for downloads')

    args = parser.parse_args()

    if args.mode == 'all':
        if not args.username:
            print("Error: --username is required when mode is 'all'")
            return

        user_url = f"https://bandcamp.com/{args.username}/following"

        artist_links = get_followed_artists(user_url)

        total_albums = sum(len(get_artist_albums(link)) for link in artist_links)
        current_count = 1

        for artist_link in artist_links:
            download_artist_albums(artist_link, total_albums, current_count, args.multi_thread)
            current_count += len(get_artist_albums(artist_link))

    elif args.mode == 'artist':
        if not args.artist_url:
            print("Error: --artist_url is required when mode is 'artist'")
            return

        album_links = get_artist_albums(args.artist_url)
        total_albums = len(album_links)
        download_artist_albums(args.artist_url, total_albums, 1, args.multi_thread)

    elif args.mode == 'album':
        if not args.album_url:
            print("Error: --album_url is required when mode is 'album'")
            return

        download_album(args.album_url, 1, 1)
    else:
        print("Invalid mode. Please select 'all', 'artist', or 'album'.")

if __name__ == "__main__":
    main()

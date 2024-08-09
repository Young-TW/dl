import requests
from bs4 import BeautifulSoup
import os
import argparse

def get_followed_artists(user_url):
    print(f"Fetching followed artists from {user_url}...")
    response = requests.get(user_url)
    if response.status_code == 200:
        print("Fetching successful!")
    else:
        print(f"Failed to fetch followed artists. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    artist_links = []

    # 找到所有被追蹤藝術家的連結
    for link in soup.find_all('div', class_='fan-image'):
        a_tag = link.find('a', href=True)
        if a_tag:
            artist_url = a_tag['href']
            artist_links.append(artist_url)
            print(f"Found artist link: {artist_url}")

    if not artist_links:
        print("No followed artists found. Please check the page structure.")
    return artist_links

def get_artist_albums(artist_url):
    print(f"Fetching albums from {artist_url}...")
    response = requests.get(artist_url)
    if response.status_code == 200:
        print("Fetching successful!")
    else:
        print(f"Failed to fetch albums. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    album_links = []

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('/track/') or href.startswith('/album/'):
            album_url = artist_url + href
            album_links.append(album_url)
            print(f"Found album link: {album_url}")

    if not album_links:
        print("No albums found. Please check the page structure.")
    return album_links

def download_album(album_url):
    album_name = album_url.split('/')[-1]
    if os.path.exists(album_name):
        print(f"Album {album_name} already downloaded. Skipping...")
        return

    command = f"bandcamp-dl \"{album_url}\""
    print(f"Downloading from {album_url}...")
    result = os.system(command)

    if result == 0:
        print(f"Download from {album_url} : success")
    else:
        print(f"Download from {album_url} : failed")

def download_artist_albums(artist_url):
    album_links = get_artist_albums(artist_url)
    for album_link in album_links:
        download_album(album_link)

def main():
    parser = argparse.ArgumentParser(description='Download albums from Bandcamp.')
    parser.add_argument('mode', choices=['all', 'artist', 'album'], help='Select download mode: "all" for all followed artists, "artist" for a single artist, "album" for a single album.')
    parser.add_argument('--username', type=str, help='The Bandcamp username (required if mode is "all")')
    parser.add_argument('--artist_url', type=str, help='The URL of the artist page (required if mode is "artist" or "album")')
    parser.add_argument('--album_url', type=str, help='The URL of the album page (required if mode is "album")')

    args = parser.parse_args()

    if args.mode == 'all':
        if not args.username:
            print("Error: --username is required when mode is 'all'")
            return

        # 使用者的 following 頁面 URL
        user_url = f"https://bandcamp.com/{args.username}/following"

        # 取得使用者追蹤的所有藝術家 URL
        artist_links = get_followed_artists(user_url)

        for artist_link in artist_links:
            download_artist_albums(artist_link)

    elif args.mode == 'artist':
        if not args.artist_url:
            print("Error: --artist_url is required when mode is 'artist'")
            return

        download_artist_albums(args.artist_url)

    elif args.mode == 'album':
        if not args.album_url:
            print("Error: --album_url is required when mode is 'album'")
            return

        download_album(args.album_url)

if __name__ == "__main__":
    main()

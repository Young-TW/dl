import requests
from bs4 import BeautifulSoup
import os
import argparse
import yt_dlp

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
    for link in soup.find_all('a', class_='sc-link-primary'):
        artist_url = link['href']
        if artist_url.startswith('/'):
            artist_url = "https://soundcloud.com" + artist_url
        artist_links.append(artist_url)
        print(f"Found artist link: {artist_url}")

    if not artist_links:
        print("No followed artists found. Please check the page structure.")
    return artist_links

def get_artist_tracks(artist_url):
    print(f"Fetching tracks from {artist_url}...")
    response = requests.get(artist_url)
    if response.status_code == 200:
        print("Fetching successful!")
    else:
        print(f"Failed to fetch tracks. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    track_links = []

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if '/tracks/' in href or '/sets/' in href:
            track_url = "https://soundcloud.com" + href
            track_links.append(track_url)
            print(f"Found track link: {track_url}")

    if not track_links:
        print("No tracks found. Please check the page structure.")
    return track_links

def download_track(track_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading from {track_url}...")
        ydl.download([track_url])

def download_artist_tracks(artist_url):
    track_links = get_artist_tracks(artist_url)
    for track_link in track_links:
        download_track(track_link)

def main():
    parser = argparse.ArgumentParser(description='Download tracks from SoundCloud.')
    parser.add_argument('mode', choices=['all', 'artist', 'track'], help='Select download mode: "all" for all followed artists, "artist" for a single artist, "track" for a single track.')
    parser.add_argument('--username', type=str, help='The SoundCloud username (required if mode is "all")')
    parser.add_argument('--artist_url', type=str, help='The URL of the artist page (required if mode is "artist" or "track")')
    parser.add_argument('--track_url', type=str, help='The URL of the track page (required if mode is "track")')

    args = parser.parse_args()

    if args.mode == 'all':
        if not args.username:
            print("Error: --username is required when mode is 'all'")
            return

        # 使用者的 following 頁面 URL
        user_url = f"https://soundcloud.com/{args.username}/following"

        # 取得使用者追蹤的所有藝術家 URL
        artist_links = get_followed_artists(user_url)

        for artist_link in artist_links:
            download_artist_tracks(artist_link)

    elif args.mode == 'artist':
        if not args.artist_url:
            print("Error: --artist_url is required when mode is 'artist'")
            return

        download_artist_tracks(args.artist_url)

    elif args.mode == 'track':
        if not args.track_url:
            print("Error: --track_url is required when mode is 'track'")
            return

        download_track(args.track_url)

if __name__ == "__main__":
    main()

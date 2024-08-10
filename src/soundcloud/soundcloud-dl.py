import os
import argparse

def get_followed_artists(user_url):
    print(f"Fetching followed artists from {user_url}...")
    command = f"soundcloud-dl --list-followings {user_url}"
    result = os.popen(command).read()

    artist_links = []

    if result:
        lines = result.strip().split('\n')
        for line in lines:
            if line.startswith("https://soundcloud.com/"):
                artist_links.append(line)
                print(f"Found artist link: {line}")
    else:
        print("No followed artists found or failed to fetch.")

    return artist_links

def download_track_or_playlist(url):
    command = f"soundcloud-dl {url}"
    print(f"Downloading from {url}...")
    result = os.system(command)

    if result == 0:
        print(f"Download from {url}: success")
    else:
        print(f"Download from {url}: failed")

def download_artist_tracks(artist_url):
    command = f"soundcloud-dl --list-tracks {artist_url}"
    print(f"Fetching tracks from {artist_url}...")
    result = os.popen(command).read()

    track_links = []

    if result:
        lines = result.strip().split('\n')
        for line in lines:
            if line.startswith("https://soundcloud.com/"):
                track_links.append(line)
                print(f"Found track link: {line}")
    else:
        print("No tracks found or failed to fetch.")

    for track_link in track_links:
        download_track_or_playlist(track_link)

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
        user_url = f"https://soundcloud.com/{args.username}"

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

        download_track_or_playlist(args.track_url)

if __name__ == "__main__":
    main()

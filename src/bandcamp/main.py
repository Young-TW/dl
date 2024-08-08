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
    command = f"bandcamp-dl \"{album_url}\""
    print(f"Downloading from {album_url}...")
    result = os.system(command)

    if result == 0:
        print(f"Download from {album_url} : success")
    else:
        print(f"Download from {album_url} : failed")

def main():
    parser = argparse.ArgumentParser(description='Download all albums from artists followed by a Bandcamp user.')
    parser.add_argument('username', type=str, help='The Bandcamp username (e.g., youngtw)')

    args = parser.parse_args()

    # 使用者的 following 頁面 URL
    user_url = f"https://bandcamp.com/{args.username}/following"

    # 取得使用者追蹤的所有藝術家 URL
    artist_links = get_followed_artists(user_url)

    for artist_link in artist_links:
        album_links = get_artist_albums(artist_link)

        for album_link in album_links:
            download_album(album_link)

if __name__ == "__main__":
    main()

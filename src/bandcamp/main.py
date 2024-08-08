import requests
from bs4 import BeautifulSoup
import os

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

    # 找到所有專輯的連結
    for link in soup.find_all('a', href=True):
        # 根據 HTML 結構，我們只需要 href 屬性以 /track/ 開頭的連結
        href = link.get('href')
        if href.startswith('/track/') or href.startswith('/album/'):
            album_url = artist_url + href
            album_links.append(album_url)
            print(f"Found album link: {album_url}")

    if not album_links:
        print("No albums found. Please check the page structure.")
    return album_links

def download_album(album_url):
    # 使用 bandcamp-dl 下載專輯
    command = f"bandcamp-dl \"{album_url}\""
    print(f"Downloading from {album_url}...")
    result = os.system(command)

    if result == 0:
        print(f"Download from {album_url} : success")
    else:
        print(f"Download from {album_url} : failed")

def main():
    # 藝術家主頁URL，請替換為你要爬取的藝術家頁面
    artist_url = "https://hitnex.bandcamp.com"

    # 取得所有專輯的URL
    album_links = get_artist_albums(artist_url)

    # 下載每一個專輯
    for link in album_links:
        download_album(link)

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import os

def get_artist_albums(artist_url):
    response = requests.get(artist_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    album_links = []

    # 找到所有專輯的連結
    for link in soup.find_all('a', class_='music-grid-item'):
        album_url = link.get('href')
        # 檢查是否是完整的URL，若不是則補上藝術家頁面
        if not album_url.startswith('http'):
            album_url = artist_url + album_url
        album_links.append(album_url)

    return album_links

def download_album(album_url):
    # 使用 bandcamp-dl 下載專輯
    command = f"bandcamp-dl \"{album_url}\""
    os.system(command)

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

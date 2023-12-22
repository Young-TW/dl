from threading import Thread
import requests
import re
import os

def downloadVideo(url):
    response = requests.get(url)
    videoName = re.sub(
        r'[/\\:*?"<>|]', '', re.search("<title>(.*?)<\/title>", response.text)[1].strip())
    for i in os.listdir("./video/"):
        if i == videoName + ".mp4":
            print(f"{videoName}.mp4 already exists")
            return
    videoUrl = re.search("video_url: '(.*?)',", response.text)[1]
    print(f"start downloading: {videoName}.mp4...")
    videoBytes = requests.get(videoUrl).content
    print(f"{videoName}.mp4 download complete")
    with open(f"./video/{videoName}.mp4", "wb") as f:
        f.write(videoBytes)

def downloadMultiVideos(videoList):
    threads = []

    for videoUrl in videoList:
        threads.append(Thread(target=downloadVideo, args=(videoUrl, )))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

with open("input.txt", encoding="UTF8") as urls:
    downloadMultiVideos(urls.read().splitlines())

if __name__ == "__main__":
    # downloadMultiVideos(urls.read().splitlines())
    print("done")
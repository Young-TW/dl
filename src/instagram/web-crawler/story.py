import requests
import time
import json
import random

def load_session_from_file(session_file):
    session = requests.Session()
    with open(session_file, 'r') as f:
        cookies = json.load(f)
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    return session

def download_instagram_stories(session, target_username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Referer': 'https://www.instagram.com/',
        'X-Instagram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest'
    }

    profile_url = f"https://www.instagram.com/{target_username}/"
    response = session.get(profile_url, headers=headers)

    if response.status_code == 200:
        print(f"Accessed profile page of {target_username}.")
    else:
        print(f"Failed to access profile page of {target_username}.")
        return

    # Add delays to mimic human behavior
    time.sleep(random.uniform(2, 5))

    stories_url = f"https://www.instagram.com/stories/{target_username}/"
    response = session.get(stories_url, headers=headers)

    if response.status_code == 200:
        print(f"Fetched stories for {target_username}.")
        # Process the stories content as needed
    else:
        print(f"Failed to fetch stories for {target_username}.")

if __name__ == "__main__":
    session_file = "your_session_file.json"  # 替換為你的 session 檔案路徑
    target_username = input("Enter the target Instagram username: ")

    session = load_session_from_file(session_file)
    download_instagram_stories(session, target_username)

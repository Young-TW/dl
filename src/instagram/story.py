import instaloader

def download_instagram_stories(target_username):
    L = instaloader.Instaloader()
    username = input("Enter the Instagram username: ")
    L.load_session_from_file(username)

    profile = instaloader.Profile.from_username(L.context, target_username)

    for story in L.get_stories(userids=[profile.userid]):
        for item in story.get_items():
            L.download_storyitem(item, target=f"{target_username}_stories")

if __name__ == "__main__":
    target_username = input("Enter the target username: ")
    download_instagram_stories(target_username)

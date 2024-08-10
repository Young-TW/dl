import instaloader
import argparse

def download_instagram_content(target_username, download_stories, download_highlights, download_posts, download_reels):
    L = instaloader.Instaloader()
    username = input("Enter your Instagram username: ")
    L.load_session_from_file(username)

    profile = instaloader.Profile.from_username(L.context, target_username)

    # 下載即時動態
    if download_stories:
        print(f"Downloading stories from {target_username}...")
        for story in L.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                L.download_storyitem(item, target=f"{target_username}_stories")

    # 下載精選即時動態
    if download_highlights:
        print(f"Downloading highlights from {target_username}...")
        for highlight in profile.get_highlights():
            for item in highlight.get_items():
                L.download_storyitem(item, target=f"{target_username}_highlights")

    # 下載貼文和 Reels
    if download_posts or download_reels:
        print(f"Downloading posts and reels from {target_username}...")
        for post in profile.get_posts():
            if download_reels and post.typename == 'GraphVideo' and post.is_video:
                print(f"Downloading Reel: {post.shortcode}")
                L.download_post(post, target=f"{target_username}_reels")
            elif download_posts and post.typename != 'GraphVideo':
                print(f"Downloading Post: {post.shortcode}")
                L.download_post(post, target=f"{target_username}_posts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Instagram stories, highlights, posts, and reels.")
    parser.add_argument("target_username", help="The target Instagram username.")
    parser.add_argument("--stories", action="store_true", help="Download stories from the target user.")
    parser.add_argument("--highlights", action="store_true", help="Download highlights from the target user.")
    parser.add_argument("--posts", action="store_true", help="Download posts from the target user.")
    parser.add_argument("--reels", action="store_true", help="Download reels from the target user.")
    parser.add_arguemnt("--all", action="store_true", help="Download all content from the target user.")

    args = parser.parse_args()

    if not args.stories and not args.highlights and not args.posts and not args.reels and not args.all:
        parser.error("You must specify at least one of --stories, --highlights, --posts, or --reels.")

    if args.all:
        download_instagram_content(args.target_username, True, True, True, True)
    else:
        download_instagram_content(args.target_username, args.stories, args.highlights, args.posts, args.reels)

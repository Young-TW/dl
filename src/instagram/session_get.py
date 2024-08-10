import instaloader

def save_instagram_session(username):
    L = instaloader.Instaloader()
    L.interactive_login(username)
    L.save_session_to_file()

if __name__ == "__main__":
    username = input("Enter the Instagram username: ")
    save_instagram_session(username)

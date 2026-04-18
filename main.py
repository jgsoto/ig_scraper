from perfil import run_perfil
from posts import run_posts
from followers import run_followers, run_following
from browser import close_browser
import json

def main():
    username = input("Ingresa el username: ").strip()

    print("\n🔎 Perfil...")
    perfil = run_perfil(username)

    print("\n📥 Posts...")
    posts = run_posts(username)

    print("\n👥 Seguidores...")
    followers = run_followers(username, limit=30)

    print("\n👥 Seguidos...")
    following = run_following(username, limit=30)

    data = {
        "perfil": perfil,
        "posts": posts,
        "followers": followers,
        "following": following
    }

    with open(f"{username}_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("\n✅ Todo listo")


if __name__ == "__main__":
    main()
    close_browser()
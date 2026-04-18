import json
from browser import get_page, close_browser
from perfil import run_perfil
from posts import run_posts
from followers import run_followers, run_following


def main():
    username = input("Ingresa el username: ").strip()

    page, context = get_page("https://www.instagram.com")

    try:
        data = {}

        # =====================
        # PERFIL
        # =====================
        try:
            print("\nPerfil...")
            data["perfil"] = run_perfil(page, username)
        except Exception as e:
            print("Error perfil:", e)
            data["perfil"] = None

        # =====================
        # POSTS
        # =====================
        try:
            print("\nPosts...")
            data["posts"] = run_posts(page, username)
        except Exception as e:
            print("Error posts:", e)
            data["posts"] = []

        # =====================
        # FOLLOWERS
        # =====================
        try:
            print("\nSeguidores...")
            data["followers"] = run_followers(page, username, limit=10)
        except Exception as e:
            print("Error followers:", e)
            data["followers"] = []

        # =====================
        # FOLLOWING
        # =====================
        try:
            print("\nSeguidos...")
            data["following"] = run_following(page, username, limit=10)
        except Exception as e:
            print("Error following:", e)
            data["following"] = []

        # =====================
        # GUARDAR
        # =====================
        with open(f"{username}_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("\n✅ Todo listo")

    finally:
        context.close()
        close_browser()


if __name__ == "__main__":
    main()
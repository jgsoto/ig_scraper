from parser import extract_stats, extract_bio
from browser import get_page

def run_perfil(username: str):
    url = f"https://www.instagram.com/{username}/"

    page, context = get_page(url)

    print("\n=== PERFIL ===")

    try:
        meta = page.locator("meta[name='description']").get_attribute("content")

        followers, following, posts = extract_stats(meta)
        bio = extract_bio(meta)

        data = {
            "username": username,
            "followers": followers,
            "following": following,
            "posts": posts,
            "bio": bio
        }

        print(data)
        return data

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        context.close()
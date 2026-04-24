from parser import extract_stats, extract_bio

def run_perfil(page, username: str):
    url = f"https://www.instagram.com/{username}/"

    print("\n=== PERFIL ===")

    try:
        page.goto(url)
        page.wait_for_timeout(3000)

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
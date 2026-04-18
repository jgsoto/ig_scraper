from playwright.sync_api import sync_playwright
import json
import re

username = input("Ingresa el username: ").strip()
url = f"https://www.instagram.com/{username}/"

def parse_number(text: str):
    if not text:
        return None

    text = text.strip().lower().replace(",", "")

    match = re.match(r"([\d\.]+)([km]?)", text)
    if not match:
        return None

    num = float(match.group(1))
    suffix = match.group(2)

    if suffix == "k":
        num *= 1_000
    elif suffix == "m":
        num *= 1_000_000

    return int(num)

def extract_stats(meta: str):
    followers = following = posts = None

    meta = meta.replace(",", "")

    # Followers
    m = re.search(r"([\d\.]+[km]?)\s+(seguidores|followers)", meta, re.IGNORECASE)
    if m:
        followers = parse_number(m.group(1))

    # Following
    m = re.search(r"([\d\.]+[km]?)\s+(siguiendo|seguidos|following)", meta, re.IGNORECASE)
    if m:
        following = parse_number(m.group(1))

    # Posts
    m = re.search(r"([\d\.]+[km]?)\s+(publicaciones|posts)", meta, re.IGNORECASE)
    if m:
        posts = parse_number(m.group(1))

    return followers, following, posts

def extract_bio(meta: str):
    """
    La bio está dentro de comillas en el meta description
    """
    match = re.search(r'"(.*?)"', meta)
    if match:
        return match.group(1)
    return None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    with open("cookies.json", "r", encoding="utf-8") as f:
        raw_cookies = json.load(f)

    cookies = [
        {
            "name": c["name"],
            "value": c["value"],
            "domain": ".instagram.com",
            "path": "/"
        }
        for c in raw_cookies
    ]

    context.add_cookies(cookies)

    page = context.new_page()
    page.goto(url, timeout=60000)

    # esperar carga del meta
    page.wait_for_timeout(5000)

    print("\n=== PERFIL ===")

    try:
        meta = page.locator("meta[name='description']").get_attribute("content")

        if not meta:
            print("❌ No se encontró meta description")
            browser.close()
            exit()

        print("\nRAW META:")
        print(meta)

        followers, following, posts = extract_stats(meta)

        bio = extract_bio(meta)

        print("\n📊 ESTADÍSTICAS")
        print("Seguidores:", followers)
        print("Seguidos:", following)
        print("Publicaciones:", posts)

        print("\n📝 DESCRIPCIÓN")
        print("Bio:", bio)

    except Exception as e:
        print("❌ Error:", e)

    browser.close()
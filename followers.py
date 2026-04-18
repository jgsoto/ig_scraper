from browser import get_page
import re

USERNAME_RE = re.compile(r"^[a-zA-Z0-9._]{1,30}$")


def open_follow_dialog(page, username, group="followers"):
    page.goto(f"https://www.instagram.com/{username}/")
    page.wait_for_timeout(4000)

    links = page.locator("header a")

    count = links.count()

    for i in range(count):
        el = links.nth(i)
        text = (el.inner_text() or "").lower()
        href = (el.get_attribute("href") or "").lower()

        if group in text or group in href or \
           ("seguidores" in text and group == "followers") or \
           ("seguidos" in text and group == "following"):
            
            el.click()
            page.wait_for_timeout(3000)
            return True

    return False


def scroll_and_collect(page, limit=50):
    import time

    users = set()

    page.wait_for_selector("div[role='dialog']", timeout=10000)

    dialog = page.locator("div[role='dialog']")

    scroll_box = None

    for i in range(dialog.locator("div").count()):
        el = dialog.locator("div").nth(i)
        try:
            overflow = el.evaluate("el => window.getComputedStyle(el).overflowY")
            if overflow in ["scroll", "auto"]:
                scroll_box = el
                break
        except:
            continue

    if not scroll_box:
        raise Exception("No se encontró contenedor scrolleable")

    last_height = 0

    while len(users) < limit:
        links = scroll_box.locator("a")

        for i in range(links.count()):
            try:
                username = links.nth(i).inner_text().strip()
                if username and len(username) <= 30:
                    users.add(username)
            except:
                continue

        try:
            scroll_box.evaluate("el => el.scrollTop = el.scrollHeight")
        except:
            print("Error en scroll, reintentando...")
            time.sleep(2)
            continue

        time.sleep(2)

        try:
            new_height = scroll_box.evaluate("el => el.scrollHeight")
        except:
            break

        if new_height == last_height:
            break

        last_height = new_height

    return list(users)[:limit]

def run_followers(username, limit=10):
    page, context = get_page("https://www.instagram.com")

    try:
        if not open_follow_dialog(page, username, "followers"):
            return []

        return scroll_and_collect(page, limit)

    finally:
        context.close()


def run_following(username, limit=10):
    page, context = get_page("https://www.instagram.com")

    try:
        print(f"\n👥 Obteniendo seguidos de {username}...")

        if not open_follow_dialog(page, username, "following"):
            print("No se pudo abrir seguidos")
            return []

        users = scroll_and_collect(page, limit)

        return users

    finally:
        context.close()
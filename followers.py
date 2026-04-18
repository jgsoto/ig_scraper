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


def scroll_and_collect(page, limit=5):
    import time

    users = set()

    page.wait_for_selector("div[role='dialog']", timeout=10000)
    dialog = page.locator("div[role='dialog']")

    # 🔑 encontrar el div scrolleable real
    scroll_box = None
    divs = dialog.locator("div")
    count = divs.count()

    for i in range(count):
        el = divs.nth(i)
        try:
            before = el.evaluate("el => el.scrollTop")
            el.evaluate("el => el.scrollTop += 100")
            after = el.evaluate("el => el.scrollTop")

            if after > before:
                scroll_box = el
                break
        except:
            continue

    if not scroll_box:
        raise Exception("No se encontró contenedor scrolleable REAL")

    same_count = 0

    while len(users) < limit:
        prev_count = len(users)

        # 🔑 SELECTOR REAL (como Selenium)
        links = scroll_box.locator(
            "a[href^='/']:not([href*='/explore']):not([href*='/p/'])"
        )

        for i in range(links.count()):
            try:
                el = links.nth(i)

                username = (el.inner_text() or "").strip()

                if not username:
                    continue

                if not USERNAME_RE.match(username):
                    continue

                users.add(username)

            except:
                continue

        try:
            scroll_box.evaluate("el => el.scrollBy(0, 400)")
        except:
            time.sleep(2)
            continue

        time.sleep(1.5)

        if len(users) == prev_count:
            same_count += 1
        else:
            same_count = 0

        if same_count >= 5:
            break

    return list(users)[:limit]

def run_followers(page, username, limit):
    if not open_follow_dialog(page, username, "followers"):
        return []
    
    followers = scroll_and_collect(page, limit)

    return followers


def run_following(page, username, limit):

    if not open_follow_dialog(page, username, "following"):
        print("No se pudo abrir seguidos")
        return []

    following = scroll_and_collect(page, limit)

    return following

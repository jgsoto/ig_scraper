from playwright.sync_api import sync_playwright
from cookies import load_cookies_playwright

def get_page(url: str, headless=False):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context()

    cookies = load_cookies_playwright()
    if cookies:
        context.add_cookies(cookies)

    page = context.new_page()
    page.goto(url, timeout=60000)
    page.wait_for_timeout(5000)

    return page, browser
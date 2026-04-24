from playwright.sync_api import sync_playwright
from cookies import load_cookies_playwright

_playwright = None
_browser = None


def get_browser(headless=True):
    global _playwright, _browser

    if _browser is None:
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(headless=headless)

    return _browser


def get_page(url: str, headless=True):
    browser = get_browser(headless)
    context = browser.new_context()

    cookies = load_cookies_playwright()
    if cookies:
        context.add_cookies(cookies)

    page = context.new_page()
    page.goto(url, timeout=60000)
    page.wait_for_timeout(5000)

    return page, context


def close_browser():
    global _browser, _playwright

    if _browser:
        _browser.close()
        _browser = None

    if _playwright:
        _playwright.stop()
        _playwright = None
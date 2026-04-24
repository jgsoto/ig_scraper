from playwright.sync_api import sync_playwright
from cookies import load_cookies_playwright

_playwright = None
_browser = None


def get_browser(headless=True):
    global _playwright, _browser

    if _browser is None:
        _playwright = sync_playwright().start()

        _browser = _playwright.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--window-size=1366,768"
            ]
        )

    return _browser


def get_page(url: str, headless=True):
    browser = get_browser(headless)

    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        viewport={
            "width": 1366,
            "height": 768
        },
        locale="es-EC"
    )

    cookies = load_cookies_playwright()

    if cookies:
        context.add_cookies(cookies)

    page = context.new_page()

    # anti-bot básico
    page.add_init_script("""
        Object.defineProperty(navigator,'webdriver',{
            get:()=>undefined
        });

        Object.defineProperty(navigator,'languages',{
            get:()=>['es-ES','es','en']
        });

        Object.defineProperty(navigator,'plugins',{
            get:()=>[1,2,3,4,5]
        });
    """)

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    try:
        page.wait_for_load_state(
            "networkidle",
            timeout=15000
        )
    except:
        pass

    page.wait_for_timeout(5000)

    # debug opcional si Instagram devuelve challenge/login
    print("Título:", page.title())
    print("URL:", page.url)

    return page, context


def close_browser():
    global _browser, _playwright

    if _browser:
        _browser.close()
        _browser = None

    if _playwright:
        _playwright.stop()
        _playwright = None
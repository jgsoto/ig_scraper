import json
import os

def load_cookies_dict():
    if not os.path.exists("cookies.json"):
        print("⚠️ No se encontró cookies.json")
        return {}

    with open("cookies.json", "r", encoding="utf-8") as f:
        raw = json.load(f)

    return {c["name"]: c["value"] for c in raw}


def load_cookies_playwright():
    cookies = load_cookies_dict()

    return [
        {
            "name": k,
            "value": v,
            "domain": ".instagram.com",
            "path": "/"
        }
        for k, v in cookies.items()
    ]
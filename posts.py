import requests
import json
from urllib.parse import quote
from datetime import datetime
from cookies import load_cookies_dict

GRAPHQL_URL = "https://www.instagram.com/graphql/query"
DOC_ID = "27621586024097412"

BASE_DATA = """
av=17841478027466950&__d=www&__user=0&__a=1&__req=5&__hs=20560.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1037589879
"""


def build_headers(username, cookies):
    return {
        "accept": "*/*",
        "accept-language": "es-US,es-419;q=0.9,es;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.instagram.com",
        "referer": f"https://www.instagram.com/{username}/",
        "user-agent": "Mozilla/5.0",
        "x-asbd-id": "359341",
        "x-bloks-version-id": "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
        "x-csrftoken": cookies.get("csrftoken", ""),
        "x-fb-friendly-name": "PolarisProfilePostsQuery",
        "x-fb-lsd": "AVo1234567890",
        "x-ig-app-id": "936619743392459",
        "x-ig-max-touch-points": "0",
        "x-root-field-name": "xdt_api__v1__feed__user_timeline_graphql_connection",
    }


def build_data(username, after=None):
    variables = {
        "data": {
            "count": 12,
            "include_reel_media_seen_timestamp": True,
            "include_relationship_info": True,
            "latest_besties_reel_media": True,
            "latest_reel_media": True,
        },
        "username": username,
        "__relay_internal__pv__PolarisImmersiveFeedChainingEnabledrelayprovider": False,
    }

    if after:
        variables["after"] = after

    return f"{BASE_DATA}&variables={quote(json.dumps(variables))}&doc_id={DOC_ID}"


def parse_post(node):
    return {
        "url": f"https://www.instagram.com/p/{node['code']}/",
        "caption": node["caption"]["text"] if node["caption"] else "Sin texto",
        "likes": node.get("like_count", 0),
        "comments": node.get("comment_count", 0),
        "views": node.get("play_count", "N/A"),
        "timestamp": node.get("taken_at"),
        "date": datetime.fromtimestamp(node["taken_at"]).strftime('%Y-%m-%d %H:%M:%S') if node.get("taken_at") else "N/A"
    }


def run_posts(username, max_pages=3):
    cookies = load_cookies_dict()

    if not cookies:
        print("No hay cookies")
        return []

    headers = build_headers(username, cookies)

    after = None
    all_posts = []

    for page in range(max_pages):
        print(f"\nPágina {page + 1}")

        data = build_data(username, after)

        response = requests.post(
            GRAPHQL_URL,
            headers=headers,
            cookies=cookies,
            data=data
        )

        if "application/json" not in response.headers.get("Content-Type", ""):
            print("Bloqueado o respuesta inválida")
            print(response.text[:200])
            break

        result = response.json()

        if not result.get("data"):
            print("Error en respuesta:", result)
            break

        timeline = result["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]

        for post in timeline["edges"]:
            all_posts.append(parse_post(post["node"]))

        page_info = timeline["page_info"]

        if not page_info["has_next_page"]:
            print("No hay más páginas")
            break

        after = page_info["end_cursor"]

    return sorted(all_posts, key=lambda x: x.get("timestamp", 0), reverse=True)
import json
import time
import random
from datetime import datetime
from urllib.parse import quote

import requests
from cookies import load_cookies_dict

# Configuración Global
GRAPHQL_URL = "https://www.instagram.com/graphql/query"
DOC_ID = "27621586024097412"

BASE_DATA = (
    "av=17841478027466950&__d=www&__user=0&__a=1&__req=5&"
    "__hs=20560.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1037589879"
)


def build_headers(username, cookies):
    return {
        "accept": "*/*",
        "accept-language": "es-US,es-419;q=0.9,es;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.instagram.com",
        "referer": f"https://www.instagram.com/{username}/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
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

    json_vars = quote(json.dumps(variables))
    return f"{BASE_DATA}&variables={json_vars}&doc_id={DOC_ID}"


def parse_post(node):
    taken_at = node.get("taken_at")
    date_str = "N/A"

    if taken_at:
        try:
            date_str = datetime.fromtimestamp(taken_at).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

    caption = node.get("caption") or {}

    return {
        "url": f"https://www.instagram.com/p/{node.get('code')}/",
        "caption": caption.get("text", "Sin texto"),
        "likes": node.get("like_count", 0),
        "comments": node.get("comment_count", 0),
        "views": node.get("play_count", "N/A"),
        "timestamp": taken_at,
        "date": date_str
    }


def request_with_retry(session, url, headers, cookies, data, retries=3):
    for attempt in range(retries):
        try:
            response = session.post(
                url,
                headers=headers,
                cookies=cookies,
                data=data,
                timeout=15
            )
            return response
        except requests.RequestException as e:
            print(f"[-] Error de red (intento {attempt+1}): {e}")
            time.sleep(2)
    return None


def run_posts(username, max_pages=3):
    cookies = load_cookies_dict()

    if not cookies:
        print("[-] Error: No se pudieron cargar las cookies.")
        return []

    headers = build_headers(username, cookies)

    session = requests.Session()

    after = None
    all_posts = []
    seen = set()

    for page in range(max_pages):
        print(f"[+] Página {page + 1}")

        data = build_data(username, after)

        response = request_with_retry(
            session, GRAPHQL_URL, headers, cookies, data
        )

        if not response:
            print("[-] Fallaron todos los intentos")
            break

        # 🔴 rate limit
        if response.status_code == 429:
            print("[-] Rate limit, esperando...")
            time.sleep(8)
            continue

        content_type = response.headers.get("Content-Type", "")

        text_lower = response.text.lower()

        if "checkpoint" in text_lower:
            print("[-] Instagram pide verificación")
            break

        if "login" in text_lower:
            print("[-] Sesión inválida")
            break

        if "application/json" not in content_type:
            print(f"[-] Respuesta inválida (Status: {response.status_code})")
            break

        # ✅ FIX CLAVE (robusto)
        try:
            result = response.json()
        except Exception:
            print("[-] Error parseando JSON")
            break

        data_json = result.get("data")

        if not data_json:
            print("[-] Error en la estructura:", result)
            break

        # 🔥 fallback robusto
        timeline = (
            data_json.get("xdt_api__v1__feed__user_timeline_graphql_connection")
            or (data_json.get("user") or {}).get("edge_owner_to_timeline_media")
            or data_json.get("user")
            or {}
        )

        if not timeline:
            print("[-] Timeline no encontrado")
            break

        edges = timeline.get("edges", [])

        if not edges:
            print("[i] No hay más posts")
            break

        for edge in edges:
            node = edge.get("node")
            if not node:
                continue

            code = node.get("code")

            if code in seen:
                continue

            seen.add(code)

            try:
                all_posts.append(parse_post(node))
            except Exception:
                continue

        page_info = timeline.get("page_info", {})

        if not page_info.get("has_next_page"):
            print("[i] No hay más páginas disponibles.")
            break

        after = page_info.get("end_cursor")

        # 🔥 delay humano
        time.sleep(random.uniform(1.5, 3.0))

    return sorted(
        all_posts,
        key=lambda x: x.get("timestamp") or 0,
        reverse=True
    )
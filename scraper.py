import requests
import json
from urllib.parse import quote
from datetime import datetime


def run_posts(username):

    # ==============================
    # 🔹 CONFIG
    # ==============================
    url = "https://www.instagram.com/graphql/query"

    # 🔹 Leer cookies desde cookies.json
    try:
        with open("cookies.json", "r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
    except Exception as e:
        print("❌ Error leyendo cookies.json:", e)
        return

    # 🔹 Convertir a formato requests (igual al que tenías)
    needed_cookies = [
        "datr",
        "ig_did",
        "ig_nrcb",
        "mid",
        "ps_l",
        "ps_n",
        "csrftoken",
        "ds_user_id",
        "sessionid",
        "wd"
    ]

    cookies = {
        c["name"]: c["value"]
        for c in raw_cookies
        if c["name"] in needed_cookies
    }

    # 🔹 Headers
    headers = {
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
        "x-fb-lsd": "AVo1234567890",  # ⚠️ actualizar si falla
        "x-ig-app-id": "936619743392459",
        "x-ig-max-touch-points": "0",
        "x-root-field-name": "xdt_api__v1__feed__user_timeline_graphql_connection",
    }

    DOC_ID = "27621586024097412"

    base_data = """
av=17841478027466950&__d=www&__user=0&__a=1&__req=5&__hs=20560.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1037589879
"""

    # ==============================
    # 🔹 FUNCIONES
    # ==============================
    def build_data(after=None):
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

        return f"{base_data}&variables={quote(json.dumps(variables))}&doc_id={DOC_ID}"

    # ==============================
    # 🔹 SCRAPING
    # ==============================
    after = None
    all_posts = []

    for page in range(3):
        print(f"\n📄 Página {page + 1}")

        data = build_data(after)
        response = requests.post(url, headers=headers, cookies=cookies, data=data)

        if "application/json" not in response.headers.get("Content-Type", ""):
            print("❌ Bloqueado o respuesta inválida")
            print(response.text[:200])
            break

        result = response.json()

        if not result.get("data"):
            print("❌ Error en respuesta:", result)
            break

        timeline = result["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]

        for post in timeline["edges"]:
            all_posts.append(post["node"])

        page_info = timeline["page_info"]

        if not page_info["has_next_page"]:
            print("No hay más páginas")
            break

        after = page_info["end_cursor"]

    # ==============================
    # 🔹 RESULTADOS
    # ==============================
    all_posts.sort(key=lambda x: x.get("taken_at", 0), reverse=True)

    print("\n=== POSTS ===")

    for node in all_posts:
        url_post = f"https://www.instagram.com/p/{node['code']}/"
        caption = node["caption"]["text"] if node["caption"] else "Sin texto"

        likes = node.get("like_count", 0)
        comments = node.get("comment_count", 0)
        views = node.get("play_count", "N/A")

        timestamp = node.get("taken_at")
        fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        print("\n-----------------------------")
        print("URL:", url_post)
        print("Fecha:", fecha)
        print("Likes:", likes)
        print("Comentarios:", comments)
        print("Views:", views)
        print("Caption:", caption[:80])
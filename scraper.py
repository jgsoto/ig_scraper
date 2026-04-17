import requests
import json
from urllib.parse import quote
from datetime import datetime

url = "https://www.instagram.com/graphql/query"

headers = {
    "accept": "*/*",
    "accept-language": "es-US,es-419;q=0.9,es;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.instagram.com",
    "referer": "https://www.instagram.com/leomessi/",
    "user-agent": "Mozilla/5.0",
    "x-asbd-id": "359341",
    "x-bloks-version-id": "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
    "x-csrftoken": "kPGFST2wsACiV97Y79oCiMDPlKqgQX3Y",
    "x-fb-friendly-name": "PolarisProfilePostsQuery",
    "x-fb-lsd": "_lDTv_4xPjdmXMx51XBkBI",
    "x-ig-app-id": "936619743392459",
    "x-ig-max-touch-points": "0",
    "x-root-field-name": "xdt_api__v1__feed__user_timeline_graphql_connection",
}

cookies = {
    "datr": "dbuCaZbd7nTbyExSWi29W6fI",
    "ig_did": "430A168F-10F3-4C32-B90D-739540F66D55",
    "ig_nrcb": "1",
    "mid": "aYuMpQALAAHXxWGvkG9PGPZSrqML",
    "ps_l": "1",
    "ps_n": "1",
    "csrftoken": "kPGFST2wsACiV97Y79oCiMDPlKqgQX3Y",
    "ds_user_id": "78135600915",
    "sessionid": "78135600915%3AigAbe2rq5kbQbw%3A22%3AAYiiQaeLA80F2R3ja12h0NrkSHg88GUHkD513Lc6vw",
    "wd": "661x599",
}

base_data = """
av=17841478027466950&__d=www&__user=0&__a=1&__req=5&__hs=20560.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1037589879&__s=ehf9j9%3Ab5azs0%3Agvp3e2&__hsi=7629853164525461990&__dyn=7xe6E5q5U5ObwKBAg5S1Dxu13wvoKewSAwHwNwcy0lW4o0B-q1ew6ywaq0yE460qe4o5-1ywOwa90Fw4Hw9O0H8jwae4UaEW2G0AEco5G0zE5W09yyES1Twoob82ZwrUdUbGw4mwr86C1mwrd6goK10xKi2K7E5y4U158KmUhw4rwXyEcE4y16wAw4Xw&__csr=hqrd95WnYG36xa2dFEGeAybvUyZqHnlfDimGGSFH_LRqHKQABGEyu4ah8GEvGhbGAXBGmqiEjADLHzDm5EmgWeXwCF7DypVpWGECehkbxjGmvzEoz8K4A5Uy9nxtadUzLwwDQ4o8EXUG3aiEnxFo-bwxUgAyEObze5AdCUKu4EcQcwUyEgwbS0ji02T5KVyxi00kk23Oii0uB01h6bw61woo-0HUJw1quEhgkw3x3pQaBglw-hFU1hk0_Ow2oomwjo18U2ywgQqt161DBxnxU-toy1GzVE4S1yw2XV802z8w69w&__hsdp=qiNREaA6BsCUpOW9wl22RyUB3ujhWVWTjgC54ES798hw9K26i9gBrTiwj8y0iG3K015qwvo&__sjsp=qiNREaA6BsCUpOW9wl6cmbykfAGuECJQQ9xhadxOi4o2rwxAyk9mZQE4O&__comet_req=7&fb_dtsg=NAftlAxnQehqW_on8TBIfYw5RFJbSZcckOElXqW9vLzUdDpYMi2OfPw%3A17853599968089360%3A1776359676&jazoest=26558&lsd=_lDTv_4xPjdmXMx51XBkBI&__spin_r=1037589879&__spin_b=trunk&__spin_t=1776463623&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfilePostsQuery&server_timestamps=true
"""

DOC_ID = "27621586024097412"


def build_data(after=None):
    variables = {
        "data": {
            "count": 12,
            "include_reel_media_seen_timestamp": True,
            "include_relationship_info": True,
            "latest_besties_reel_media": True,
            "latest_reel_media": True,
        },
        "username": "leomessi",
        "__relay_internal__pv__PolarisImmersiveFeedChainingEnabledrelayprovider": False,
    }

    if after:
        variables["after"] = after

    variables_encoded = quote(json.dumps(variables))

    return f"{base_data}&variables={variables_encoded}&doc_id={DOC_ID}"


# 🚀 PAGINACIÓN
after = None

for page in range(1):

    data = build_data(after)

    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    result = response.json()

    timeline = result["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]
    posts = timeline["edges"]

    all_posts = []

    for page in range(3):
        data = build_data(after)
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        result = response.json()

        timeline = result["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]
        posts = timeline["edges"]

        for post in posts:
            all_posts.append(post["node"])

        page_info = timeline["page_info"]

        if not page_info["has_next_page"]:
            break

        after = page_info["end_cursor"]

# 🔥 ORDENAR AQUÍ
all_posts.sort(key=lambda x: x.get("taken_at", 0), reverse=True)

# 🔥 IMPRIMIR
for node in all_posts:
    url_post = f"https://www.instagram.com/p/{node['code']}/"
    caption = node["caption"]["text"] if node["caption"] else "Sin texto"

    likes = node.get("like_count", 0)
    comments = node.get("comment_count", 0)
    views = node.get("play_count", "N/A")
    media_type = node.get("media_type")

    timestamp = node.get("taken_at")
    fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

    print("URL:", url_post)
    print("Fecha:", fecha)
    print("Likes:", likes)
    print("Comentarios:", comments)
    print("Views:", views)
    print("Tipo:", media_type)
    print("Caption:", caption[:80])
    print("=" * 60)

    page_info = timeline["page_info"]

    if not page_info["has_next_page"]:
        print("No hay más páginas")
        break

    after = page_info["end_cursor"]

import re

def parse_number(text: str):
    if not text:
        return None

    text = text.strip().lower().replace(",", "")
    match = re.match(r"([\d\.]+)([km]?)", text)

    if not match:
        return None

    num = float(match.group(1))
    suffix = match.group(2)

    if suffix == "k":
        num *= 1_000
    elif suffix == "m":
        num *= 1_000_000

    return int(num)


def extract_stats(meta: str):
    followers = following = posts = None
    meta = meta.replace(",", "")

    patterns = {
        "followers": r"([\d\.]+[km]?)\s+(seguidores|followers)",
        "following": r"([\d\.]+[km]?)\s+(siguiendo|seguidos|following)",
        "posts": r"([\d\.]+[km]?)\s+(publicaciones|posts)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, meta, re.IGNORECASE)
        if match:
            value = parse_number(match.group(1))
            if key == "followers":
                followers = value
            elif key == "following":
                following = value
            elif key == "posts":
                posts = value

    return followers, following, posts


def extract_bio(meta: str):
    match = re.search(r'"(.*?)"', meta)
    return match.group(1) if match else None
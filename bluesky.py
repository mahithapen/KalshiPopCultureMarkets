import requests
from typing import Optional, Tuple, List, Dict

def search_bluesky_posts(
    jwt: str,
    query: str,
    limit: int = 25,
    cursor: Optional[str] = None,
    sort: str = "latest",
    lang: Optional[str] = "en"
) -> Tuple[List[Dict], Optional[str]]:
    headers = {"Authorization": f"Bearer {jwt}"}
    params = {"q": query, "limit": limit, "sort": sort}
    if cursor:
        params["cursor"] = cursor
    if lang:
        params["lang"] = lang

    resp = requests.get(API_BASE, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # print(data)

    posts = []
    for hit in data.get("posts", []):
        rec = hit
        posts.append({
            "uri":        rec["uri"],
            "author":     hit["author"]["handle"],
            "text":       rec["record"].get("text", ""),
            "created_at": rec["record"]["createdAt"],
            "reply_count":   rec["replyCount"],
            "like_count":    rec["likeCount"],
            "repost_count":  rec["repostCount"]
        })

    return posts, data.get("cursor")

PDS_URL  = "https://bsky.social"            # make sure this matches where your account lives
USERNAME = "timmyjunchen.bsky.social"        # include the “.bsky.social” suffix
PASSWORD = "Abcd1234" # use an App-Password if you have 2FA enabled
API_BASE = f"{PDS_URL}/xrpc/app.bsky.feed.searchPosts"

url     = f"{PDS_URL}/xrpc/com.atproto.server.createSession"
headers = {"Content-Type": "application/json"}
payload = {"identifier": USERNAME, "password": PASSWORD}

resp = requests.post(url, json=payload, headers=headers, timeout=10)

data = resp.json()
access_jwt = data["accessJwt"]
refresh_jwt = data.get("refreshJwt")  # for refreshing later, if needed

print("Logged in! Access JWT:", access_jwt)

posts, next_cursor = search_bluesky_posts(
        jwt=access_jwt,
        query="Thunderbolts",
        limit=10,
        sort="latest",
        lang="en"
    )

for p in posts:
    print(f"[{p['created_at']}] @{p['author']} ({p['like_count']}❤) {p['text']}\n")

if next_cursor:
    print("More available! Pass cursor=", next_cursor, "to fetch the next page.")
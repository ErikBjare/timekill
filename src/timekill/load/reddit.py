"""
Load content from reddit
"""
import json
import os
from pathlib import Path

import joblib
import praw
import requests

from ..models import Content

memory = joblib.Memory("cache", verbose=0)

feeds_dir = Path(__file__).parent.parent.parent / "data" / "feeds"


@memory.cache
def load_reddit(subreddit: str, limit=100, t="week"):
    feedfile = feeds_dir / "reddit" / subreddit / "top.json"

    if os.environ.get("REDDIT_CLIENT_ID"):
        print("Loading from praw")
        return load_reddit_praw(subreddit, limit, t)
    if feedfile.exists():
        print("Loading from cache")
        return _parse_json(json.loads(feedfile.read_text()))

    # fallback, hits ratelimits often
    print("Loading from json-request")
    return load_reddit_json(subreddit, limit, t)


def load_reddit_json(subreddit, limit, t) -> list[Content]:
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t={t}"
    print(url)
    r = requests.get(url, timeout=10)
    data = r.json()
    if "error" in data:
        raise Exception(data)
    assert data["kind"] == "Listing"
    return _parse_json(data)


def _parse_json(data):
    content = []
    shorten_desc = True
    for item in data["data"]["children"]:
        desc = item["data"]["selftext"]
        if shorten_desc:
            desc = desc.split("\n")[0]
        content.append(
            Content(
                title=item["data"]["title"],
                description=desc,
                url=item["data"]["url"],
                source_url=f"https://www.reddit.com{item['data']['permalink']}",
            )
        )
    return content


# Load latest posts from reddit
def load_reddit_praw(subreddit, limit, t) -> list[Content]:
    """
    Load latest posts from reddit
    """
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="python3:timekill:0.1 (by /u/ErikBjare)",
    )
    content = []
    for submission in reddit.subreddit(subreddit).top(limit=limit, time_filter=t):
        content.append(
            Content(
                title=submission.title,
                description=submission.selftext,
                url=submission.url,
                source_url=f"https://www.reddit.com{submission.permalink}",
            )
        )
    return content


if __name__ == "__main__":
    print(load_reddit("python"))

"""Collect recent updates from an RSS/Atom feed."""

import feedparser
import requests

CHROME_RELEASES_FEED = "https://chromereleases.googleblog.com/feeds/posts/default"
USER_AGENT = "QA-Signal/0.1 (portfolio project; QA change monitoring)"
TIMEOUT_SECONDS = 15


def fetch_feed(url: str) -> list[dict]:
    """Download a feed and return a list of raw entries.

    Returns an empty list (instead of crashing) if anything goes wrong.
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"[ERROR] Could not fetch {url}: {error}")
        return []

    parsed = feedparser.parse(response.content)

    if parsed.bozo and not parsed.entries:
        print(f"[ERROR] Feed from {url} could not be parsed.")
        return []

    entries = []
    for entry in parsed.entries:
        entries.append(
            {
                "title": entry.get("title", "(no title)"),
                "published": entry.get("published", None),
                "link": entry.get("link", None),
                "summary": entry.get("summary", ""),
            }
        )
    return entries


if __name__ == "__main__":
    items = fetch_feed(CHROME_RELEASES_FEED)
    print(f"Fetched {len(items)} entries from Chrome Releases\n")

    for item in items[:5]:
        print(f"Title:     {item['title']}")
        print(f"Published: {item['published']}")
        print(f"Link:      {item['link']}")
        print(f"Summary:   {item['summary'][:150]}...")
        print("-" * 60)
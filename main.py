import feedparser
import requests
from datetime import datetime
import os

SENT_FILE = "sent_urls.txt"
FEEDS_FILE = "feeds.txt"


def load_already_sent_articles():
    """Load URLs of articles already sent to Discord."""
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r") as file:
        return set(file.read().splitlines())


def add_already_sent_article(url):
    """Add a URL to the sent list without overwriting existing entries."""
    with open(SENT_FILE, "a") as file:  # append mode
        file.write(url + "\n")


def send_discord_message(content: str):
    """Send a message to Discord via webhook."""
    data = {"content": content}
    response = requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json=data)

    if response.status_code == 204:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")


def load_feeds():
    """Load RSS feed URLs from feeds.txt."""
    if not os.path.exists(FEEDS_FILE):
        return set()
    with open(FEEDS_FILE, "r") as file:
        return file.read().splitlines()


def list_items_from_feed(feed_url, sent_articles):
    """Check the feed for today's articles and send new ones to Discord."""
    parsed = feedparser.parse(feed_url)
    feed_title = getattr(parsed.feed, "title", "Unknown Blog")

    today_str = datetime.now().strftime("%d %b %Y")

    for entry in parsed.entries:
        pub_date = getattr(entry, "published", None) or getattr(entry, "pubDate", None) or "Unknown date"
        article_id = getattr(entry, "link", None)

        if not article_id:
            continue  # skip entries without link

        if today_str in pub_date and article_id not in sent_articles:
            print("Article published today, sending message...")
            message = (
                f"Blog title: {feed_title}\n"
                f"Title: {getattr(entry, 'title', 'No title')}\n"
                f"Link: {article_id}\n"
                f"PubDate: {pub_date}"
            )
            send_discord_message(message)
            add_already_sent_article(article_id)
            sent_articles.add(article_id)  # update in-memory set to avoid duplicates in same run


if __name__ == "__main__":
    sent_articles = load_already_sent_articles()
    feeds = load_feeds()
    for feed in feeds:
        list_items_from_feed(feed, sent_articles)

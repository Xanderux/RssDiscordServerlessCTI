import feedparser
from datetime import datetime
import requests
from secrets import DISCORD_WEBHOOK_URL

def send_discord_message(content: str):
    data = {
        "content": content
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("✅ Message has been send !")
    else:
        print(f"❌ Error {response.status_code} : {response.text}")

def feeds():
    with open("feeds.txt", "r") as file :
        feeds = file.read().splitlines()
    return feeds

def list_item_feed(feed_url):
    parsed = feedparser.parse(feed_url)
    for entry in parsed.entries :
        channel = parsed.channel
        pub_date = getattr(entry, "published", None) or getattr(entry, "pubDate", None) or "Unknown date"

        today_str = datetime.now().strftime("%d %b %Y")
        if today_str in pub_date :
            print(f"Article has been published today, should trigger message")
            message = (
                f"Blog title : {channel.title}\n"
                f"Title : {entry.title}\n"
                f"Link : {entry.link}\n"
                f"PubDate : {pub_date}"
            )
            send_discord_message(message)

if __name__ == "__main__":
    feeds = feeds()
    for feed in feeds :
        list_item_feed(feed)

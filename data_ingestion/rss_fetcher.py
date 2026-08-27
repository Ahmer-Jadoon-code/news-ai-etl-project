import feedparser

def fetch_raw_feed(url):
    """URL se raw RSS feed fetch karta hai."""
    try:
        feed = feedparser.parse(url)
        return feed
    except Exception as e:
        print(f"❌ Error fetching feed from {url}: {e}")
        return None
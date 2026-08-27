import sys
import os
from datetime import datetime

# Current folder ko system path mein add karna taake config aur fetcher import ho sakein
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config import RSS_FEEDS
from rss_fetcher import fetch_raw_feed

def scrape_articles():
    """Teeno sources se data la kar structured dictionary banata hai."""
    all_articles = []
    
    for source, url in RSS_FEEDS.items():
        print(f"Fetching news from {source}...")
        raw_feed = fetch_raw_feed(url)
        
        if raw_feed and raw_feed.entries:
            for entry in raw_feed.entries:
                article = {
                    "source": source,
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published_at": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "ingestion_timestamp": datetime.now().isoformat()
                }
                all_articles.append(article)
                
    print(f"\n✅ Total {len(all_articles)} articles scraped successfully!")
    return all_articles

if __name__ == "__main__":
    print("Starting Ingestion...\n")
    data = scrape_articles()
    
    # Test ke liye pehli news print karwa rahe hain
    if data:
        print("\n--- Pheli News Ka Sample ---")
        for key, value in data[0].items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    from data_storage.s3_handler import upload_raw_to_s3
    from data_warehouse.snow_client import load_raw_to_snowflake
    
    print("Starting Ingestion...\n")
    data = scrape_articles()
    
    if data:
        # 1. S3 Bronze Layer mein upload
        file_name = f"raw_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        print(f"\nUploading {len(data)} articles to S3 Bronze Layer...")
        upload_raw_to_s3(data, file_name)
        
        # 2. Snowflake Bronze Layer mein insert
        print(f"Loading {len(data)} articles into Snowflake Bronze Layer...")
        load_raw_to_snowflake(data)
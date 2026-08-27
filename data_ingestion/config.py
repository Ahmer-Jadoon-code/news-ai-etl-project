import os
from dotenv import load_dotenv

# Root folder ka path nikal kar .env load karna
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_dir, '.env'))

# AWS & Snowflake Configurations (Aage ke liye)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# RSS Feeds List
RSS_FEEDS = {
    "yahoo": "https://finance.yahoo.com/news/rssindex",
    "cnbc": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
    "marketwatch": "http://feeds.marketwatch.com/marketwatch/topstories/"
}
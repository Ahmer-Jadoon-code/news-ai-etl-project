import snowflake.connector
import os
import sys
from dotenv import load_dotenv

# Root folder se .env load karna
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_dir, '.env'))

def get_snowflake_connection():
    """Snowflake se connection banata hai"""
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

def load_raw_to_snowflake(data):
    """Raw JSON data ko Snowflake ki Bronze table mein insert karta hai"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS BRONZE_NEWS_RAW (
            source VARCHAR, title VARCHAR, link VARCHAR, published_at VARCHAR, summary VARCHAR, ingestion_timestamp VARCHAR
        )
        """
        cursor.execute(create_table_query)
        insert_query = """
        INSERT INTO BRONZE_NEWS_RAW (source, title, link, published_at, summary, ingestion_timestamp) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values_to_insert = [(item.get('source'), item.get('title'), item.get('link'), item.get('published_at'), item.get('summary'), item.get('ingestion_timestamp')) for item in data]
        cursor.executemany(insert_query, values_to_insert)
        conn.commit()
        print(f"✅ Success: {len(values_to_insert)} records loaded into Snowflake BRONZE table.")
    except Exception as e:
        print(f"❌ Snowflake Error (Bronze): {e}")
    finally:
        cursor.close()
        conn.close()

def load_silver_to_snowflake(data):
    """Cleaned JSON data ko Snowflake ki Silver table mein insert karta hai"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS SILVER_NEWS_CLEANED (
            source VARCHAR, title VARCHAR, link VARCHAR, published_at VARCHAR, summary VARCHAR, ingestion_timestamp VARCHAR
        )
        """
        cursor.execute(create_table_query)
        insert_query = """
        INSERT INTO SILVER_NEWS_CLEANED (source, title, link, published_at, summary, ingestion_timestamp) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values_to_insert = [(item.get('source'), item.get('title'), item.get('link'), item.get('published_at'), item.get('summary'), item.get('ingestion_timestamp')) for item in data]
        cursor.executemany(insert_query, values_to_insert)
        conn.commit()
        print(f"✅ Success: {len(values_to_insert)} records loaded into Snowflake SILVER table.")
    except Exception as e:
        print(f"❌ Snowflake Error (Silver): {e}")
    finally:
        cursor.close()
        conn.close()

def load_gold_to_snowflake(data):
    """AI Enriched JSON data ko Snowflake ki Gold table mein insert karta hai"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        # 1. Gold table banayen jisme AI ka Sentiment aur Summary bhi ho
        create_table_query = """
        CREATE TABLE IF NOT EXISTS GOLD_NEWS_ANALYTICS (
            source VARCHAR, title VARCHAR, link VARCHAR, published_at VARCHAR, summary VARCHAR, 
            ingestion_timestamp VARCHAR, sentiment VARCHAR, ai_summary VARCHAR
        )
        """
        cursor.execute(create_table_query)
        
        insert_query = """
        INSERT INTO GOLD_NEWS_ANALYTICS 
        (source, title, link, published_at, summary, ingestion_timestamp, sentiment, ai_summary) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values_to_insert = [
            (
                item.get('source'), item.get('title'), item.get('link'), item.get('published_at'), 
                item.get('summary'), item.get('ingestion_timestamp'), item.get('sentiment'), item.get('ai_summary')
            ) 
            for item in data
        ]
        
        cursor.executemany(insert_query, values_to_insert)
        conn.commit()
        print(f"✅ Success: {len(values_to_insert)} records loaded into Snowflake GOLD_NEWS_ANALYTICS table.")
        
    except Exception as e:
        print(f"❌ Snowflake Error (Gold): {e}")
    finally:
        cursor.close()
        conn.close()
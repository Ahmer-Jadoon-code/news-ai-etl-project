import pandas as pd

def clean_bronze_data(raw_data):
    """Bronze layer ke raw data ko Pandas ke zariye clean karta hai."""
    
    if not raw_data:
        print("No data to clean.")
        return []

    # 1. List of dictionaries ko Pandas DataFrame mein convert karein
    df = pd.DataFrame(raw_data)
    print(f"Original data count: {len(df)}")

    # 2. Duplicates remove karein (Agar ek hi link dobara aaye)
    df.drop_duplicates(subset=['link'], keep='first', inplace=True)
    
    # 3. Missing (Null) titles ya summaries ko handle karein
    df.fillna({'title': 'No Title', 'summary': 'No Summary Available'}, inplace=True)

    # 4. Dates ko proper format mein layen
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce').astype(str)

    print(f"Cleaned data count: {len(df)}")
    
    # Wapas DataFrame ko dictionary ki list mein convert karein taake S3/Snowflake mein load ho sake
    cleaned_data = df.to_dict(orient='records')
    
    return cleaned_data
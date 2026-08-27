import boto3
import json
import os
import sys

# Root folder ko path mein add karna taake config import ho sake
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from data_ingestion.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME

def upload_raw_to_s3(data, file_name):
    """Data ko JSON format mein S3 ke raw (Bronze) folder mein upload karta hai"""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1'
        )
        s3_key = f"raw/{file_name}"
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME, Key=s3_key, Body=json.dumps(data, indent=4), ContentType='application/json'
        )
        print(f"✅ Success: Raw Data uploaded to s3://{S3_BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"❌ S3 Raw Upload Error: {e}")

def upload_silver_to_s3(data, file_name):
    """Cleaned Data ko JSON format mein S3 ke silver folder mein upload karta hai"""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1'
        )
        s3_key = f"silver/{file_name}"
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME, Key=s3_key, Body=json.dumps(data, indent=4), ContentType='application/json'
        )
        print(f"✅ Success: Cleaned Data uploaded to s3://{S3_BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"❌ S3 Silver Upload Error: {e}")

def upload_gold_to_s3(data, file_name):
    """AI Enriched Data ko JSON format mein S3 ke gold folder mein upload karta hai"""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1'
        )
        s3_key = f"gold/{file_name}"
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME, Key=s3_key, Body=json.dumps(data, indent=4), ContentType='application/json'
        )
        print(f"✅ Success: Gold Data uploaded to s3://{S3_BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"❌ S3 Gold Upload Error: {e}")
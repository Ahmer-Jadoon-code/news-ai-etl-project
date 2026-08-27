from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

# Project root ko path mein add karna taake humari purani files import ho sakein
sys.path.append('/opt/airflow/project_code')

# --- IMPORTS ---
from data_ingestion.scrap import scrape_articles
from data_storage.s3_handler import upload_raw_to_s3, upload_silver_to_s3, upload_gold_to_s3
from data_warehouse.snow_client import load_raw_to_snowflake, load_silver_to_snowflake, load_gold_to_snowflake
from data_processing.clean_data import clean_bronze_data
from data_processing.enrich_data import enrich_silver_data


def run_bronze_pipeline(**kwargs):
    """Task 1: Scrape news and load into Bronze Layer"""
    print("Starting Bronze Ingestion Pipeline...")
    data = scrape_articles()
    
    if data:
        file_name = f"raw_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        upload_raw_to_s3(data, file_name)
        load_raw_to_snowflake(data)
        return data  # Silver ke liye bheja
    return []

def run_silver_pipeline(**kwargs):
    """Task 2: Clean data and load into Silver Layer"""
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids='ingest_to_bronze_layer')
    
    if not raw_data:
        print("No raw data found.")
        return []

    print("Starting Silver Layer Processing...")
    cleaned_data = clean_bronze_data(raw_data)
    
    if cleaned_data:
        file_name = f"silver_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        upload_silver_to_s3(cleaned_data, file_name)
        load_silver_to_snowflake(cleaned_data)
        return cleaned_data  # Gold ke liye bheja
    return []

def run_gold_pipeline(**kwargs):
    """Task 3: Enrich data using AI and load into Gold Layer"""
    ti = kwargs['ti']
    silver_data = ti.xcom_pull(task_ids='process_silver_layer')
    
    if not silver_data:
        print("No silver data found to enrich. Stopping Gold layer.")
        return

    print("Starting Gold Layer (AI Enrichment)...")
    enriched_data = enrich_silver_data(silver_data)
    
    if enriched_data:
        file_name = f"gold_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        upload_gold_to_s3(enriched_data, file_name)
        load_gold_to_snowflake(enriched_data)
        print("🏆 Full Medallion Pipeline Complete!")
    else:
        print("AI Processing ke baad koi data nahi bacha.")


default_args = {
    'owner': 'ahmer',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'news_full_medallion_pipeline',
    default_args=default_args,
    description='Full Medallion Pipeline: Bronze -> Silver -> Gold (AI)',
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    task_bronze = PythonOperator(
        task_id='ingest_to_bronze_layer',
        python_callable=run_bronze_pipeline,
    )

    task_silver = PythonOperator(
        task_id='process_silver_layer',
        python_callable=run_silver_pipeline,
    )

    task_gold = PythonOperator(
        task_id='enrich_to_gold_layer',
        python_callable=run_gold_pipeline,
    )

    # --- FULL MEDALLION ARCHITECTURE FLOW ---
    task_bronze >> task_silver >> task_gold
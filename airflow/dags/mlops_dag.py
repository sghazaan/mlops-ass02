from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from extract_and_clean import extract_and_clean
import pandas as pd

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'mlops_dag',
    default_args=default_args,
    description='MLOps DAG for data extraction, cleaning, and storage',
    schedule_interval=None,  # Set the schedule as per your requirement
)

# Task to extract and clean data
def extract_clean_data(**kwargs):
    url = kwargs['url']  # Pass the URL as an argument
    data = extract_and_clean(url)
    return data

extract_clean_task = PythonOperator(
    task_id='extract_clean_task',
    python_callable=extract_clean_data,
    op_kwargs={'url': 'https://www.dawn.com/'},  # Change URL as needed
    dag=dag,
)

# Task to store data in CSV
def store_data_to_csv(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='extract_clean_task')
    df = pd.DataFrame(data)
    df.to_csv('/opt/airflow/dags/extracted_data.csv', index=False)  # Change path as needed

store_csv_task = PythonOperator(
    task_id='store_csv_task',
    python_callable=store_data_to_csv,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
extract_clean_task >> store_csv_task

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Définition du DAG
with DAG('drug_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',  # Exécuter quotidiennement (modifiable)
         catchup=False) as dag:

    # Étape d'extraction
    def extract_task():
        drugs, pubmed_csv, pubmed_json, clinical_trials = extract_data()
        return drugs, pubmed_csv, pubmed_json, clinical_trials

    # Étape de transformation
    def transform_task(ti):
        drugs, pubmed_csv, pubmed_json, clinical_trials = ti.xcom_pull(task_ids='extract_task')
        pubmed_csv_mentions, pubmed_json_mentions, clinical_trials_mentions = transform_data(drugs, pubmed_csv, pubmed_json, clinical_trials)
        return pubmed_csv_mentions, pubmed_json_mentions, clinical_trials_mentions

    # Étape de chargement
    def load_task(ti):
        pubmed_csv_mentions, pubmed_json_mentions, clinical_trials_mentions = ti.xcom_pull(task_ids='transform_task')
        load_data(pubmed_csv_mentions, clinical_trials_mentions)

    # Définir les opérateurs Python
    extract_op = PythonOperator(
        task_id='extract_task',
        python_callable=extract_task,
    )

    transform_op = PythonOperator(
        task_id='transform_task',
        python_callable=transform_task,
    )

    load_op = PythonOperator(
        task_id='load_task',
        python_callable=load_task,
    )

    # Orchestration des tâches
    extract_op >> transform_op >> load_op

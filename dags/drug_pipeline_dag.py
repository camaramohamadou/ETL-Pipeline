from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from etl.extract import extract_data
from etl.transform import transform_data, find_top_journal, find_related_drugs_in_pubmed
from etl.load import load_data
from etl.log_config import setup_logger

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG('drug_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    logger = setup_logger()  # Initialiser le logger

    # Tâche d'extraction
    def extract_task():
        logger.info("Début de l'extraction")
        try:
            return extract_data()
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction : {e}")
            raise

    # Tâche de transformation
    def transform_task(ti):
        logger.info("Début de la transformation")
        try:
            drugs, pubmed_csv, pubmed_json, clinical_trials = ti.xcom_pull(task_ids='extract_task')
            return transform_data(drugs, pubmed_csv, pubmed_json, clinical_trials)
        except Exception as e:
            logger.error(f"Erreur lors de la transformation : {e}")
            raise

    # Tâche de chargement
    def load_task(ti):
        logger.info("Début du chargement")
        try:
            pubmed_csv_mentions, clinical_trials_mentions = ti.xcom_pull(task_ids='transform_task')
            load_data(pubmed_csv_mentions, clinical_trials_mentions)
        except Exception as e:
            logger.error(f"Erreur lors du chargement : {e}")
            raise

    #  Trouver le journal avec le plus de mentions de médicaments
    def top_journal_task(ti):
        logger.info("Recherche du journal mentionnant le plus de médicaments")
        pubmed_csv_mentions = ti.xcom_pull(task_ids='transform_task')[0]
        top_journal = find_top_journal(pubmed_csv_mentions.to_dict(orient='records'))
        logger.info(f"Le journal qui mentionne le plus de médicaments est : {top_journal}")

    # Tâche de recherche des Médicaments associés dans PubMed mais pas dans Clinical Trials
    def related_drugs_task(ti):
        logger.info("Recherche des médicaments liés dans PubMed mais pas dans Clinical Trials")
        pubmed_csv_mentions, clinical_trials_mentions = ti.xcom_pull(task_ids='transform_task')
        related_drugs = find_related_drugs_in_pubmed('Aspirin', pubmed_csv_mentions.to_dict(orient='records'), clinical_trials_mentions.to_dict(orient='records'))
        logger.info(f"Médicaments associés à Aspirin : {related_drugs}")

    # Définition des opérateurs Python
    extract_op = PythonOperator(
        task_id='extract_task',
        python_callable=extract_task
    )

    transform_op = PythonOperator(
        task_id='transform_task',
        python_callable=transform_task
    )

    load_op = PythonOperator(
        task_id='load_task',
        python_callable=load_task
    )

    top_journal_op = PythonOperator(
        task_id='top_journal_task',
        python_callable=top_journal_task
    )

    related_drugs_op = PythonOperator(
        task_id='related_drugs_task',
        python_callable=related_drugs_task
    )

    # Ordonnancement des tâches
    extract_op >> transform_op >> [load_op, top_journal_op, related_drugs_op]

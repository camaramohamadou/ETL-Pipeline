from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from etl.log_config import setup_logger

if __name__ == "__main__":
    logger = setup_logger()  # Initialisation du logger

    logger.info("Début du pipeline ETL")

    # Extraction
    try:
        logger.info("Début de l'étape d'extraction")
        drugs, pubmed_csv, pubmed_json, clinical_trials = extract_data()
        logger.info("Extraction terminée avec succès")
    except Exception as e:
        logger.error(f" Erreur lors de l'extraction des données: {e}")

    # Transformation
    try:
        logger.info("Début de l'étape de transformation")
        pubmed_csv_mentions, pubmed_json_mentions, clinical_trials_mentions = transform_data(drugs, pubmed_csv, pubmed_json, clinical_trials)
        logger.info("Transformation terminée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la transformation des données: {e}")

    # Chargement
    try:
        logger.info("Début de l'étape de chargement")
        load_data(pubmed_csv_mentions, clinical_trials_mentions)
        logger.info("Chargement terminé avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données: {e}")

    logger.info("Fin du pipeline ETL")

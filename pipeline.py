from etl.extract import extract_data
from etl.transform import transform_data, find_top_journal, find_related_drugs_in_pubmed
from etl.load import load_data
from etl.log_config import setup_logger

def main():
    logger = setup_logger()  # Initialisation du logger

    logger.info("Début du pipeline ETL")

    # Étape 1 : Extraction des données
    try:
        logger.info("Extraction des données")
        drugs, pubmed_csv, pubmed_json, clinical_trials = extract_data()
        logger.info("Extraction terminée")
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction : {e}")
        return

    # Étape 2 : Transformation des données
    try:
        logger.info("Transformation des données")
        pubmed_csv_mentions, pubmed_json_mentions, clinical_trials_mentions = transform_data(drugs, pubmed_csv, pubmed_json, clinical_trials)
        logger.info("Transformation terminée")
    except Exception as e:
        logger.error(f"Erreur lors de la transformation : {e}")
        return

    # Appel des nouvelles fonctions
    try:
        logger.info("Recherche du journal mentionnant le plus de médicaments")
        top_journal = find_top_journal(pubmed_csv_mentions.to_dict(orient='records'))
        logger.info(f"Le journal qui mentionne le plus de médicaments est : {top_journal}")

        logger.info("Recherche des médicaments liés à un médicament donné dans PubMed")
        related_drugs = find_related_drugs_in_pubmed('Aspirin', pubmed_csv_mentions.to_dict(orient='records'), clinical_trials_mentions.to_dict(orient='records'))
        logger.info(f"Les médicaments liés à Aspirin dans PubMed mais pas dans Clinical Trials sont : {related_drugs}")
    except Exception as e:
        logger.error(f"Erreur lors de la recherche des informations spécifiques : {e}")

    # Étape 3 : Chargement des données
    try:
        logger.info("Chargement des données")
        load_data(pubmed_csv_mentions, clinical_trials_mentions)
        logger.info("Pipeline terminé avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du chargement : {e}")

if __name__ == "__main__":
    main()

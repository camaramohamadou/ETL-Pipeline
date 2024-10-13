from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

if __name__ == "__main__":
    # Extraction
    drugs, pubmed_csv, pubmed_json, clinical_trials = extract_data()

    # Transformation
    pubmed_csv_mentions, pubmed_json_mentions, clinical_trials_mentions = transform_data(drugs, pubmed_csv, pubmed_json, clinical_trials)

    # Chargement (création et sauvegarde du graphe JSON)
    load_data(pubmed_csv_mentions, clinical_trials_mentions)

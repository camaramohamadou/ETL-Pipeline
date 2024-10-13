import pandas as pd
import json
import yaml

def load_config(config_file='conf/config.yml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_csv(file_path):
    """
    charge un fichier csv dans un dataframe pandas
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV {file_path}: {e}")
        return None

def load_json(file_path):
    """
    charge un fichier json dans un dataframe pandas
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return pd.json_normalize(data)  # Convertir en DataFrame si nécessaire par pandas
    except Exception as e:
        print(f"Erreur lors du chargement du fichier JSON {file_path}: {e}")
        return None


def extract_data():
    """
    fonction d'extraction des données 
    """
    config = load_config()

    drugs = load_csv(config['input_paths']['drugs'])
    pubmed_csv = load_csv(config['input_paths']['pubmed_csv'])
    pubmed_json = load_json(config['input_paths']['pubmed_json'])
    clinical_trials = load_csv(config['input_paths']['clinical_trials'])

    return drugs, pubmed_csv, pubmed_json, clinical_trials

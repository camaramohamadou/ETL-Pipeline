import pandas as pd
import json
import yaml

def load_config(config_file='conf/config.yml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV {file_path}: {e}")
        return None

def load_json(file_path):
    """
    Load a JSON file into a Python dictionary or pandas DataFrame.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return pd.json_normalize(data)  # Convertir en DataFrame si nécessaire
    except Exception as e:
        print(f"Erreur lors du chargement du fichier JSON {file_path}: {e}")
        return None


def extract_data():
    config = load_config()

    drugs = load_csv(config['input_paths']['drugs'])
    pubmed_csv = load_csv(config['input_paths']['pubmed_csv'])
    pubmed_json = load_json(config['input_paths']['pubmed_json'])
    clinical_trials = load_csv(config['input_paths']['clinical_trials'])

    return drugs, pubmed_csv, pubmed_json, clinical_trials

# def extract_data():
#     """
#     Extract data from all the required sources.
#     """
#     drugs = load_csv('data/input/drugs.csv')
#     pubmed_csv = load_csv('data/input/pubmed.csv')
#     pubmed_json = load_json('data/input/pubmed.json')
#     clinical_trials = load_csv('data/input/clinical_trials.csv')
    
#     return drugs, pubmed_csv, pubmed_json, clinical_trials

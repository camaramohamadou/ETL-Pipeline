import pandas as pd

def clean_data(df):
    """
    Nettoyage des donnees entrees (suppression des valeurs manquantes, etc.)
    """
    df_cleaned = df.dropna()
    return df_cleaned

def find_drug_mentions(drugs_df, articles_df, title_col):
    """
    pour chaque article (ou essai clinique), identifier les médicaments mentionnés dans le titre.
    Retourne un DataFrame avec l'ID de l'article, le titre, le journal, la date et les médicaments mentionnés.
    """
    mentions = []
    for index, row in articles_df.iterrows():
        mentioned_drugs = [drug for drug in drugs_df['drug'] if drug.lower() in row[title_col].lower()]
        if mentioned_drugs:
            mentions.append({
                'id': row['id'],
                'title': row[title_col],
                'journal': row['journal'],
                'date': row['date'],
                'mentioned_drugs': mentioned_drugs
            })
    return pd.DataFrame(mentions)

def transform_data(drugs, pubmed_csv, pubmed_json, clinical_trials):
    """
    applique le nettoyage et la transformation aux données extraites
    """
    # Nettoyage des données
    drugs_cleaned = clean_data(drugs)
    pubmed_csv_cleaned = clean_data(pubmed_csv)
    pubmed_json_cleaned = clean_data(pubmed_json)
    clinical_trials_cleaned = clean_data(clinical_trials)
    
    # Identification des mentions de médicaments dans PubMed (CSV et JSON) et Clinical Trials
    pubmed_csv_mentions = find_drug_mentions(drugs_cleaned, pubmed_csv_cleaned, 'title')
    pubmed_json_mentions = find_drug_mentions(drugs_cleaned, pubmed_json_cleaned, 'title')
    clinical_trials_mentions = find_drug_mentions(drugs_cleaned, clinical_trials_cleaned, 'scientific_title')
    
    return pubmed_csv_mentions, pubmed_json_mentions, clinical_trials_mentions

# Fonctions pour la recherche du journal mentionnant le plus de médicaments
def find_top_journal(json_data):
    """
    Extraire le nom du journal qui mentionne le plus de médicaments différents.
    """
    journal_drug_count = {}

    # Parcours des journaux dans les données JSON
    for record in json_data:
        journal = record['journal']
        drugs = set(record['mentioned_drugs'])  # Utilisation d'un ensemble pour éviter les doublons
        if journal not in journal_drug_count:
            journal_drug_count[journal] = drugs
        else:
            journal_drug_count[journal].update(drugs)

    # Trouver le journal avec le plus de mentions de médicaments différents
    top_journal = max(journal_drug_count, key=lambda k: len(journal_drug_count[k]))
    return top_journal

# Fonctions pour la recherche des mêmes médicaments dans PubMed mais pas dans Clinical Trials 
def find_related_drugs_in_pubmed(drug, json_data, clinical_trials_data):
    """
    Pour un médicament donné, trouver tous les autres médicaments mentionnés par les mêmes journaux
    dans PubMed, mais pas dans Clinical Trials.
    """
    pubmed_journals = set()  # Journaux où le médicament est mentionné dans PubMed
    clinical_trial_journals = set(record['journal'] for record in clinical_trials_data)

    # Trouver les journaux où le médicament est mentionné dans PubMed
    for record in json_data:
        if drug in record['mentioned_drugs']:
            pubmed_journals.add(record['journal'])

    # Éliminer les journaux qui apparaissent dans Clinical Trials
    relevant_journals = pubmed_journals - clinical_trial_journals

    # Trouver tous les autres médicaments mentionnés dans ces journaux
    related_drugs = set()
    for record in json_data:
        if record['journal'] in relevant_journals:
            related_drugs.update(record['mentioned_drugs'])

    # Supprimer le médicament original de la liste des médicaments associés
    related_drugs.discard(drug)
    return related_drugs

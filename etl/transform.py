import pandas as pd

def clean_data(df):
    """
    Clean the input DataFrame (drop missing values, etc.)
    """
    df_cleaned = df.dropna()
    return df_cleaned

def find_drug_mentions(drugs_df, articles_df, title_col):
    """
    For each article (or clinical trial), identify which drugs are mentioned in the title.
    Returns a DataFrame with the article ID, title, journal, date, and mentioned drugs.
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
    Apply cleaning and transformation to the extracted data.
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

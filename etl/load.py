import json

def create_drug_graph(pubmed_mentions, clinical_trials_mentions):
    """
    Créer un graphe de liaison entre les médicaments et les journaux avec les dates associées.
    """
    graph = {}

    # Fonction pour ajouter des mentions au graphe
    def add_mentions_to_graph(mentions_df):
        for _, row in mentions_df.iterrows():
            for drug in row['mentioned_drugs']:
                if drug not in graph:
                    graph[drug] = []
                graph[drug].append({
                    'journal': row['journal'],
                    'date': row['date']
                })

    # Ajouter les mentions des articles PubMed
    add_mentions_to_graph(pubmed_mentions)
    
    # Ajouter les mentions des essais cliniques
    add_mentions_to_graph(clinical_trials_mentions)

    return graph

def save_graph_to_json(graph, output_path='data/output/drug_graph.json'):
    """
    Sauvegarder le graphe sous format JSON.
    """
    try:
        with open(output_path, 'w') as outfile:
            json.dump(graph, outfile, indent=4)
        print(f"Graphe sauvegardé dans {output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du graphe JSON : {e}")

def load_data(pubmed_mentions, clinical_trials_mentions):
    """
    Fonction principale pour créer et sauvegarder le graphe JSON.
    """
    graph = create_drug_graph(pubmed_mentions, clinical_trials_mentions)
    save_graph_to_json(graph)

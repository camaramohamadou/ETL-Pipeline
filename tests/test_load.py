import unittest
import os
import pandas as pd  # Importation manquante de pandas
from etl.load import create_drug_graph, save_graph_to_json

class TestLoad(unittest.TestCase):

    def test_create_drug_graph(self):
        # Données fictives pour le test
        pubmed_mentions = pd.DataFrame({
            'journal': ['Journal A'],
            'date': ['2021-01-01'],
            'mentioned_drugs': [['Aspirin']]
        })
        clinical_trials_mentions = pd.DataFrame({
            'journal': ['Journal B'],
            'date': ['2021-01-02'],
            'mentioned_drugs': [['Ibuprofen']]
        })

        graph = create_drug_graph(pubmed_mentions, clinical_trials_mentions)
        self.assertIn('Aspirin', graph)
        self.assertIn('Ibuprofen', graph)

    def test_save_graph_to_json(self):
        # Test que le graphe est sauvegardé
        graph = {'Aspirin': [{'journal': 'Journal A', 'date': '2021-01-01'}]}
        save_graph_to_json(graph, output_path='data/output/test_graph.json')
        self.assertTrue(os.path.exists('data/output/test_graph.json'))

if __name__ == '__main__':
    unittest.main()

import unittest
import pandas as pd
from etl.transform import find_drug_mentions

class TestTransform(unittest.TestCase):

    def setUp(self):
        # Données fictives pour le test
        self.drugs_df = pd.DataFrame({'drug': ['Aspirin', 'Ibuprofen']})
        self.articles_df = pd.DataFrame({
            'id': [1, 2],
            'title': ['Aspirin is great', 'Ibuprofen is better'],
            'journal': ['Journal A', 'Journal B'],
            'date': ['2021-01-01', '2021-01-02']
        })

    def test_find_drug_mentions(self):
        # Test que les mentions de médicaments sont bien identifiées
        mentions_df = find_drug_mentions(self.drugs_df, self.articles_df, 'title')
        self.assertEqual(len(mentions_df), 2)  # Les deux médicaments sont mentionnés

if __name__ == '__main__':
    unittest.main()

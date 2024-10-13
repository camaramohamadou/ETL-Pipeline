import unittest
from etl.extract import load_csv, load_json

class TestExtract(unittest.TestCase):

    def test_load_csv(self):
        # Test que le fichier CSV est chargé correctement
        df = load_csv('data/input/drugs.csv')
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

    def test_load_json(self):
        # Test que le fichier JSON est chargé correctement
        df = load_json('data/input/pubmed.json')
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()

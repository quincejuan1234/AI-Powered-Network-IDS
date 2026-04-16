import unittest
import pandas as pd

from src.features import clean_column_names


class TestFeatures(unittest.TestCase):
    def test_clean_column_names(self):
        df = pd.DataFrame({" A ": [1], " B ": [2]})
        cleaned = clean_column_names(df)
        self.assertEqual(cleaned.columns.tolist(), ["A", "B"])


if __name__ == "__main__":
    unittest.main()

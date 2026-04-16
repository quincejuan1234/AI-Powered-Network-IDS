import unittest
import pandas as pd

from src.preprocess import preprocess_dataframe


class TestPreprocess(unittest.TestCase):
    def test_preprocess_dataframe(self):
        df = pd.DataFrame(
            {
                " Flow Duration ": [10, 20, 30],
                "Tot Fwd Pkts": [1, 2, 3],
                "Label": ["BENIGN", "DDoS", "BENIGN"],
            }
        )

        processed = preprocess_dataframe(df)

        self.assertIn("Flow Duration", processed.columns)
        self.assertIn("Tot Fwd Pkts", processed.columns)
        self.assertIn("Label", processed.columns)
        self.assertEqual(set(processed["Label"].unique()), {0, 1})


if __name__ == "__main__":
    unittest.main()

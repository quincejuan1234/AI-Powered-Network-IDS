import unittest
import pandas as pd


class TestPredictShape(unittest.TestCase):
    def test_dataframe_creation(self):
        df = pd.DataFrame({"Flow Duration": [1, 2], "Tot Fwd Pkts": [3, 4]})
        self.assertEqual(df.shape, (2, 2))


if __name__ == "__main__":
    unittest.main()

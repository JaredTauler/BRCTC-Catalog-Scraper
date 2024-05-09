import unittest
from scraping import fetchNAVOID


class TestfetchNAVOID(unittest.TestCase):
    def test_length(self):
        result = fetchNAVOID()
        self.assertTrue(
            len(result) == 3,
            f"NAVOID should be 3 digits long. Got {len(result)}."
        )

    def test_isnumeric(self):
        result = fetchNAVOID()
        self.assertTrue(
            result.isnumeric,
            f"NAVOID should be numeric. Got {result}."
        )


if __name__ == '__main__':
    unittest.main()

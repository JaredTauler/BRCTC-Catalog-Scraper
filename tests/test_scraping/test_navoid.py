import unittest
from scraping import fetchNAVOID


class TestfetchNAVOID(unittest.TestCase):
    def test_length(self):
        result = fetchNAVOID()
        self.assertTrue(
            len(result) == 3
        )

    def test_isnumeric(self):
        result = fetchNAVOID()
        self.assertTrue(
            result.isnumeric
        )


if __name__ == '__main__':
    unittest.main()

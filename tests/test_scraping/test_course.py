import unittest
from scraping.course import getSoup
from scraping.course import getReq

class Test_getSoup(unittest.TestCase):
    def test_length(self):
        result = getSoup(14456)
        self.assertTrue(
            len(result) == 3
        )

class TestgetReq(unittest.TestCase):
    def test_length(self):
        result = getReq()
        self.assertTrue(
            len(result) == 3
        )

    # def test_isnumeric(self):
    #     result = fetchNAVOID()
    #     self.assertTrue(
    #         result.isnumeric
    #     )


if __name__ == '__main__':
    unittest.main()

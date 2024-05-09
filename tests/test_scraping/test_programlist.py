import unittest
from scraping.programlist import fetchPrograms
from common import is_string_empty

class Test_fetchPrograms(unittest.TestCase):
    def setUp(self) -> None:
        self.result = fetchPrograms()

    def test_list_length(self):
        self.assertGreater(
            l := len(self.result),
            100,
            f"Expected there to be more programs, only got {l}."
        )

    def test_values(self):
        for poid, name in self.result:
            # POID
            self.assertTrue(
                len(poid) == 4,
                f"Expected program ID to be 4 digits, got {len(poid)}."
            )

            self.assertTrue(
                poid.isnumeric(),
                f"Expected program ID to be numeric, got {poid}."
            )

            # Name
            self.assertFalse(
                is_string_empty(name),
                f"Expected name to not be blank."
            )

            self.assertTrue(
                len(name.split()) > 1,
                f"Expected name to have more than one space, got {name}."
            )


if __name__ == '__main__':
    unittest.main()

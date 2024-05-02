from scraping.programlist import fetchPrograms

import unittest
from scraping.corelist import fetchCores
from scraping.corelist import fetchCourses

programs = fetchPrograms()

class Test_fetchCores(unittest.TestCase):
    def test_core_structure_and_length(self):
        for poid, program_name in programs:
            cores = list(fetchCores(poid))

            # All A.A.S. should have more than 0 cores.
            # Somre programs have 0 cores so this is a good way to check there are actually cores running through
            if "A.A.S." in program_name:
                self.assertTrue(
                    len(cores) > 0
                )

            # Check structure
            for id, name, course_soups in cores:
                # Check ID
                self.assertTrue(
                    id[:5] == "core_"
                )
                self.assertTrue(
                    id[5:].isnumeric()
                )
                self.assertFalse(
                    id.isspace()
                )

                # Check name
                self.assertFalse(
                    name.isspace()
                )

                self.assertTrue(
                    len(name.split()) > 0
                )

                # Courses
                self.assertTrue(
                    len(course_soups),
                    0

                )

                for course_soup in course_soups:
                    self.assertFalse(
                        course_soup.text.isspace()

                    )

# class Test_fetchCourses(unittest.TestCase):
#     def test_course(self):
#         for poid, _ in programs:
#             for _, _, course_soups in fetchCores(poid):
#                 for soup in course_soups:
#                     courses = fetchCourses(soup)


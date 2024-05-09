from scraping.programlist import fetchPrograms
from common import is_string_empty

import unittest
import scraping.corelist as corelist
from scraping.corelist import fetchCourses

programs = fetchPrograms()


class Test_getProgramCores(unittest.TestCase):
    def setUp(self) -> None:
        self.out = []
        for poid, _ in programs:
            for core_soup in corelist.getProgramCores(poid):
                self.out.append(core_soup)

    def test_outputisnone(self):
        self.assertTrue(
            len(self.out) > 0,
            "Function returned no cores."
        )

    def test_elementisnone(self):
        for core_soup in self.out:
            self.assertTrue(
                core_soup is not None,
                "Core soup cannot be none."
            )


class Test_processCoreSoup(unittest.TestCase):
    def setUp(self) -> None:
        self.list_of_core_soup = []

        for poid, _ in programs:
            result = corelist.getProgramCores(poid)
            self.list_of_core_soup.append(result)

    def test_process(self):
        for l in self.list_of_core_soup:
            for soup in l:
                result = corelist.processCoreSoup(soup)
                if result is not None:
                    id, name, course_soups = result
                    self.assertTrue(
                        id[:5] == "core_",
                        f"core ID should start with 'core_'. Got {id}"
                    )
                    self.assertTrue(
                        id[5:].isnumeric(),
                        f"Core ID should be numeric. Got {id}"
                    )
                    self.assertFalse(
                        is_string_empty(id),
                        f"Core ID should not be blank."
                    )

                    # Check name
                    self.assertFalse(
                        is_string_empty(name),
                        f"Core name should not be blank"
                    )

                    # Courses
                    self.assertTrue(
                        len(course_soups) > 0,
                        f"There should be at least 1 course soup"
                    )

                    # Course list_of_core_soup is HTML relating to a core's course.
                    for course_soup in course_soups:
                        self.assertFalse(
                            is_string_empty(course_soup.text),
                            f"Course soup should not be blank."
                        )


class Test_fetchCores(unittest.TestCase):
    def setUp(self) -> None:
        self.output = []

        for poid, _ in programs:
            for core in corelist.fetchCores(poid):
                self.output.append(core)

    def test_programs(self):
        for poid, program_name in programs:
            cores = list(corelist.fetchCores(poid))
            # All A.A.S. should have more than 0 cores.
            # Some programs have 0 cores so this is a good way to check there are actually cores running through
            if "A.A.S." in program_name:
                self.assertTrue(
                    len(cores) > 0,
                    f"An A.A.S. program has 0 cores."
                )


class Test_fetchCourses(unittest.TestCase):
    def setUp(self) -> None:
        self.output = []

        for poid, _ in programs:
            for core in corelist.fetchCores(poid):
                self.output.append(core)

    def test_courses(self):
        for _, _, course_soups in self.output:
            for soup in course_soups:
                print(soup)
                result = fetchCourses(soup)
                # TODO add some tests
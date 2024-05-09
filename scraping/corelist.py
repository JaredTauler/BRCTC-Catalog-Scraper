from bs4 import BeautifulSoup
from .common import fetchSoup
from common import is_string_empty


def processCoreSoup(soup: BeautifulSoup):
    """
    No if statements or checks. Good data must be passed in by design.
    """
    # TODO Acquire through id?
    h = soup.find(['h2', 'h3', 'h4'])  # Get header

    name = h.text
    id = h.find_all("a")[1]['id']

    # "Concentrations Header" and other headers that contain no ul need to be filtered out.
    courses = soup.find_all("li", class_=["acalog-course", "acalog-adhoc-list-item"])

    return id, name, courses


def getProgramCores(poid):
    url = f"http://catalog.blueridgectc.edu/preview_program.php?poid={poid}"
    soup = fetchSoup(url, f"{poid}cores")

    cores = soup.find_all(class_="acalog-core")  # Get all cores

    for core in cores:
        # Check if core contains a course
        core_courses = core.find("li", class_=["acalog-course", "acalog-adhoc-list-item"])
        # Yield the CORE (a soup) if so
        if core_courses:
            yield core


# Get list of cores pertaining to a program.
def fetchCores(poid: str):
    """
    Yield a list of cores (groupings of courses)
    :param poid: A program's ID
    :return: str, str, BeautifulSoup: Core ID, name, and bs4 object containing a list of courses
    """
    for core_soup in getProgramCores(poid):
        if result := processCoreSoup(core_soup):
            yield result


def fetchCourses(ul: BeautifulSoup) -> []:
    """
    Get lists of courses from a list_of_core_soup unordered list of courses.FIXME

    Because or+and: need to look ahead. Meaning no fancy smancy generator oh nosies!

    :param core: BeautifulSoup: ul html element containing acaolog-courses
    :return:
    [str], [str], [str]: Coid, coid that are :OR: with eachother, coid that are "AND" with eachother
    """

    courses = {}

    or_blocks = []
    and_blocks = []

    current_or_block = []
    current_and_block = []

    # Give nonconforming courses their own """unique""" id, in case for whatever reason they are used in an OR or AND
    nonconform_coid = -1

    for li in ul:
        li = BeautifulSoup(
            str(li),
            'html.parser'
        )

        # acalog-course
        course_id_element = li.find('a', onclick=True)

        # First, get ID.
        if course_id_element:
            onclick_value = course_id_element['onclick']
            # Find coid
            coid = onclick_value[18:23]  # FIXME: very stupid.

            courses[coid] = {}

        # Nonconforming option
        elif not is_string_empty(li.text) and not li.find('table'):  # FIXME a bit icky

            coid = str(nonconform_coid)
            nonconform_coid -= 1  # IMPORTANT! de-increment this to keep them unique.

            courses[coid] = {}
            courses[coid]['nonconforming'] = li.text

        # Invalid il
        else:
            print("SKIPPING", li) # FIXME better alert?
            continue

        state = li.text.split()[-1]

        # Determine "OR"
        if state == "OR":
            current_or_block.append(coid)

        # Time to create a new block
        elif len(current_or_block) > 0:
            current_or_block.append(coid)
            or_blocks.append(current_or_block)
            current_or_block = []

        # Determine "AND"
        if state == "AND":
            current_and_block.append(coid)

        elif len(current_and_block) > 0:
            current_and_block.append(coid)
            and_blocks.append(current_and_block)
            current_and_block = []

    # TODO fix?
    return {
        'courses': courses,
        'or_blocks': or_blocks,
        'and_blocks': and_blocks
    }

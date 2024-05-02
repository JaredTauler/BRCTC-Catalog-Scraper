from bs4 import BeautifulSoup
from .common import getSoup, CATOID


def getCores(poid: str):
    """
    Create a list of cores (groupings of courses)
    :param poid: A program's ID
    :return: str, str, BeautifulSoup: Core ID, name, and bs4 object containing a list of courses
    """
    url = f"http://catalog.blueridgectc.edu/preview_program.php?catoid={CATOID}&poid={poid}"
    soup = getSoup(url, f"{poid}cores")  # FIXME

    for core in soup.find_all(class_="acalog-core"):
        # TODO more than h3 and h4 headers contain courses?
        # Try to find header on acaolog-core element
        h = core.find('h3')
        if h is None:  # acalog-core can either be an h3 or h4 element, they both hold acaolog-course elements
            h = core.find('h4')

        if h is not None:
            name = h.text
            id = h.find_all("a")[1]['id']

            # "Concentrations Header" and other headers that contain no ul need to be filtered out.
            courses = core.find_all("li")
            if courses != []:
                yield id, name, courses


def getCourses(ul: BeautifulSoup) -> []:
    """
    Get lists of courses from a soup unordered list of courses.FIXME

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
        elif not li.text.isspace() and not li.find('table'):  # FIXME a bit icky
            coid = str(nonconform_coid)
            nonconform_coid -= 1  # IMPORTANT! de-increment this to keep them unique.

            courses[coid] = {}
            courses[coid]['nonconforming'] = li.text

        # Invalid il
        else:
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

    return {
        'courses': courses,
        'or_blocks': or_blocks,
        'and_blocks': and_blocks
    }


# TODO for debug
def fetchCore(poid, i):
    for j, data in enumerate(getCores(poid)):
        # print(data)
        if j == i:
            print(i)
            return data[0], data[1], getCourses(data[2])


# Get list of cores pertaining to a program.
def fetchCores(poid):
    for id, name, course_soup in getCores(poid):
        yield id, name, getCourses(course_soup)

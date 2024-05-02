from .common import fetchSoup, CATOID


# print(md.Course)

# FIXME a bit icky
def getReq(string, soup):
    req = []
    coid_or = []
    coid_and = []
    is_poid = []  # FIXME hotfix

    current_or_block = []
    current_and_block = []
    # With requisite sections, section starts with one of the strings, and it stops at the first <br> element
    start = soup.find_all(string=string)  # Starting element
    if not start:  # Req is not present in this course
        return
    start = start[0]

    stop = start.find_next("br")

    # Finding elems in range
    current_element = start
    while current_element != stop:
        current_element = current_element.find_next()  # Move to next element

        # Found an element that belongs to reqs were looking for. Yay!!
        if current_element.get('href'):
            href_value = current_element['href']
            coid = href_value.split('&coid=')[-1]

            if not coid.isnumeric():  # dealing with program requisite
                coid = href_value.split('&poid=')[-1]
                is_poid.append(coid)

            req.append(coid)  # FIXME is it possible for a reqs to not have this??

            # Same logic as seen in courselist

            # Determine or
            # next_sibling gets text elements too, which we need to catch ", or"s and ", and"s
            if 'or' in current_element.next_sibling.next_sibling:
                current_or_block.append(coid)

            # Time to create a new block
            elif len(current_or_block) > 0:
                coid_or.append(
                    current_or_block + [coid]
                )
                current_or_block = []

            # Determine and
            if 'and' in current_element.next_sibling.next_sibling:
                current_and_block.append(coid)

            elif len(current_and_block) > 0:
                coid_and.append(
                    current_and_block + [coid]
                )
                current_and_block = []

    return {
        'id': req,
        'or': coid_or,
        'and': coid_and,
        'poid': is_poid
    }


def getReqs(soup):
    option = {
        'pre': 'Prerequisite(s): ',
        'co': 'Corequisite(s): ',
        'preco': 'Prerequisite/Corequisite(s): '
    }
    option_value = {

    }
    for k, v in option.items():
        option_value[k] = getReq(v, soup)

    return option_value


# FIXME this is fucked up on 14896
# kind of stupid probably fine
def getDesc(soup):
    h3_elements = soup.find_all('h3')
    header = h3_elements[0]

    string = ""
    for s in header.next_siblings:
        match s.name:
            case None:
                string += s
            case 'a':
                href_value = s['href']
                coid = href_value.split('&coid=')[-1]
                string = string[1:-1]  # extra space on either side for some reason
                string += f'&{coid}'  # TODO probably okay way to do this
            case 'br':
                break

    return string

def getSoup(coid):
    url = f"http://catalog.blueridgectc.edu/ajax/preview_course.php?coid={coid}&show"
    return fetchSoup(url, f"{coid}fetchcourse")

# Get course details, and ID's of related courses
def fetchCourse(coid):
    soup = getSoup(coid)

    # Get course name
    h3_elements = soup.find_all('h3')
    name = h3_elements[0].get_text()

    # Get reqs
    req = getReqs(soup)

    # Get course description
    description = getDesc(soup)

    return name, req, description

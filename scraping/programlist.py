from .common import fetchSoup, NAVOID


def getSoup():
    url = f"http://catalog.blueridgectc.edu/content.php?navoid={NAVOID}"
    return fetchSoup(url, "program")


def fetchPrograms():
    """
     Get a list of programs the college provides

    :return: poid, name
    """
    soup = getSoup()
    program_lists = soup.find_all(class_="program-list")

    found = []
    for program_list in program_lists:
        # Extract the <a> tags within each <ul>
        links = program_list.find_all('a')

        for link in links:
            # Extract 'poid' from the href attribute
            href = link.get('href')
            poid = href.split('poid=')[1].split('&')[0] if 'poid=' in href else None

            # Extract class name
            name = link.text.strip()

            found.append(
                (poid, name)
            )
    return found

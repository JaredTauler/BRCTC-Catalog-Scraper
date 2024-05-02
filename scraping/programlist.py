from .common import getSoup, CATOID, NAVOID


def fetchPrograms():
    """
     Get a list of programs the college provides

    :return: poid, name
    """
    url = f"http://catalog.blueridgectc.edu/content.php?navoid={NAVOID}"

    soup = getSoup(url, "program")
    program_lists = soup.find_all(class_="program-list")

    found_programs = []
    # Programs
    for program_list in program_lists:
        # Extract the <a> tags within each <ul>
        links = program_list.find_all('a')

        for link in links:
            # Extract 'poid' from the href attribute
            href = link.get('href')
            poid = href.split('poid=')[1].split('&')[0] if 'poid=' in href else None

            # Extract class name
            name = link.text.strip()

            yield poid, name

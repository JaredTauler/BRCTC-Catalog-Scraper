from .common import getSoup


from bs4 import BeautifulSoup
import requests

def fetchPrograms():
    """
     Acquire NAVOID

    # :return: poid, name
    """
    url = f"http://catalog.blueridgectc.edu/"

    soup = getSoup(url, "program")
    nav = soup.find_all(id="acalog-navigation")

    # found_programs = []
    # # Programs
    # for program_list in program_lists:
    #     # Extract the <a> tags within each <ul>
    #     links = program_list.find_all('a')
    #
    #     for link in links:
    #         # Extract 'poid' from the href attribute
    #         href = link.get('href')
    #         poid = href.split('poid=')[1].split('&')[0] if 'poid=' in href else None
    #
    #         # Extract class name
    #         name = link.text.strip()
    #
    #         yield poid, name
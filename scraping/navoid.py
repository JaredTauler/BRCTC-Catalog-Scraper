from .common import getSoup


def fetchNAVOID():
    """
     Acquire NAVOID

    :return: NAVOID id
    :rtype: str
    """
    url = f"http://catalog.blueridgectc.edu/"

    soup = getSoup(url, "navoid")
    nav = soup.find_all(id="acalog-navigation")[0]

    # check for the text program in each nav element
    for element in nav:
        if "program" in element.text.lower():
            a = element.find("a")
            navoid = a.attrs['href'][-3:]
            return navoid

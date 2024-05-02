from bs4 import BeautifulSoup
import requests

import time

# WAIT_TIME = 3 # seconds

# Acalog catalog ID. Every year on catalog.blueridge.edu gets a different catoid.
CATOID = 23 # FIXME future proof

# Navigation element belonging to "Academic Programs"
NAVOID = 622 # FIXME futureproof navoid, this changes every year too.

# Get a soup to do operations on, from a URL.
# def getSoup(url):
#     time.sleep(WAIT_TIME) # FIXME add wait time to prevent being blocked
#     print("OUT")
#     response = requests.get(url)
#     return BeautifulSoup(
#         response.content.decode("utf-8"), 'html.parser'
#     )


# TODO FIXME
import debugging
# def getSoup(url):
#     # time.sleep(WAIT_TIME)
#     # print("OUT")
#     # response = requests.get(url)
#     # debugging.pickle_dump("html", response)
#     response = debugging.pickle_load("html")
#     return BeautifulSoup(
#         response.content.decode("utf-8"), 'html.parser'
#     )


def getSoup(url, name):
    try:
        response = debugging.pickle_load(name)
    except:
        time.sleep(1)
        print("GOING OUT")
        response = requests.get(url)
        debugging.pickle_dump(name, response)

    return BeautifulSoup(
        response.content.decode("utf-8"), 'html.parser'
    )


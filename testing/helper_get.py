import populate as pop
# import scraping as sr
from db_inter import db
import db_inter.models as md

from pony.orm.core import db_session

db.bind(provider='sqlite', filename='../db.sqlite', create_db=True) # FIXME
db.generate_mapping(create_tables=True)

# 1608
# import webapp.app as help
import webapp.app.helper as help

# gp = help.getProgram()

# seen_course = {}
d = help.getProgram(13)

from pprint import pprint
pprint(d)


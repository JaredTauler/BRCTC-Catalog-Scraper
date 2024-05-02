import populate as pop
# import scraping as sr
from db_inter import db
import db_inter.models as md

from pony.orm.core import db_session

db.bind(provider='sqlite', filename=':memory:', create_db=True)
db.generate_mapping(create_tables=True)
c = pop.getCourse(
    14850
)

# import webapp.app as help
import webapp.app.helper as help

# gp = help.getProgram()

# seen_course = {}
d = help.processCourse(
    c
)

from pprint import pprint
pprint(d)


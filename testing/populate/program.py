import populate as pop
# import scraping as sr
from db_inter import db
import db_inter.models as md
from pprint import pprint
from pony.orm.core import db_session
import scraping as sr

# Very evil lol
# def dictslice(d,i,j):
#     return dict(
#         zip(
#             list(d.keys())[i:j],
#             list(d.values())[i:j]
#         )
#     )

db.bind(provider='sqlite', filename=':memory:', create_db=True)
db.generate_mapping(create_tables=True)

# Get program
with db_session:
    pop.populateProgramList()

    program = pop.getProgram(1608)

    core_id, core_name, courses = sr.fetchCore(1671, 1)
    q = pop.populateCore(
        core_id,
        core_name,
        courses,
    program
    )

    id_ = md.Program.select().where(poid=1608).fetch()[0].id

import webapp.app.helper as help

gp = help.getProgram(id_)
with db_session:
    # print(md.CoreCourse.select().fetch())
    for i in md.CoreCourse.select().fetch():
        # if i.id > 6 and i.id < 11:
            name = i.course.name
            if name:
                print(name)
            _or = [i.id for i in i.or_]
            _and = [i.id for i in i.and_]
            print(f"{i.id}: \n  or: {_or}\n  and: {_and}")


# pprint(gp['core'])

# # import webapp.app as help
# import webapp.app.helper as help
#
# # gp = help.getProgram()4
#
# # seen_course = {}
# d = help.processCourse(
#     c
# )
#
# from pprint import pprint
# pprint(d)
#
#
# 1608

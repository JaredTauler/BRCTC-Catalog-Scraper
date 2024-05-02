from pony.orm.core import db_session

from db_inter import db

import scraping as sr
import db_inter.models as md


def setToList(set, callback=None):
    e = set.order_by(1).fetch()
    return e

@db_session
def populateProgramList():
    for poid, name in sr.fetchPrograms():
        md.Program(name=name, poid=poid)

    db.commit()


@db_session
def getProgram(poid):
    return md.Program.select().where(poid=poid).first()


def exclude(l, target):
    return [x for x in l if x != target]


# FIXME probably not most efficient :/
def processReq(r, the_course):
    req_type, req_data = r

    idmap = {}  # quick little dict of rel_id: relationship
    # Process courses
    if req_data:
        for req_coid in req_data['id']:
            if req_coid in req_data['poid']:
                # FIXME SUPER DUPER HOTFIX AAAAAA (program req)
                new_req = md.Requisite(
                    # coid=req_coid,
                    course=the_course,
                    # req_course=getCourse(req_coid),
                    req_program=getProgram(req_coid),
                    type_=req_type
                )
            else:
                new_req = md.Requisite(
                    # coid=req_coid,
                    course=the_course,
                    req_course=getCourse(req_coid),
                    type_=req_type
                )
            the_course.requisites.add(new_req)

            idmap[req_coid] = new_req

        # Process or + and:

        # Return related req, but not self
        def relationship(l):  # ❤ owo
            for block in l:
                for rel_coid in block:
                    for c in exclude(block, rel_coid):
                        yield rel_coid, c

        for rel in relationship(req_data['and']):
            idmap[rel[0]].and_.add(
                idmap[rel[1]]
            )

        for rel in relationship(req_data['or']):
            idmap[rel[0]].or_.add(
                idmap[rel[1]]
            )


def getCourse(coid):
    def queryCourse(coid):
        return md.Course.select().where(coid=coid).first()

    with db_session:
        the_course = queryCourse(coid)
        if not the_course:  # Course is not in DB.
            name, req, description = sr.fetchCourse(coid)
            the_course = md.Course(coid=coid, name=name, description=description)
            # Process reqs:
            for r in req.items():
                processReq(r, the_course)

    return the_course


from pprint import pprint


# FIXME this is shitty
@db_session
def populateCore(
        core_id, core_name, courses, program
):
    def exclude(l, target):
        return [x for x in l if x != target]

    new_core = md.Core(
        core_id=core_id,
        name=core_name,
        program=program  # Add core to program
    )

    coidmap = {}
    # Create course objects
    for coid, property in courses['courses'].items():
        # Create new course object
        if v := property.get("nonconforming"):
            new_core_course = md.CoreCourse(
                nonconforming=v
            )
        else:
            new_core_course = md.CoreCourse(
                course=getCourse(coid)
            )

        coidmap[coid] = new_core_course

        new_core.courses.add(
            new_core_course
        )

    # Add and properties to courses
    for rel_block in courses['and_blocks']:
        for coid in rel_block:
            for rel_coid in exclude(rel_block, coid):
                coidmap[coid].and_.add(
                    coidmap[rel_coid]
                )

    # add "or" property
    for rel_block in courses['or_blocks']:
        for coid in rel_block:  # For every course
            in_relationship_with = exclude(rel_block, coid)
            # Add ORs to all sibling courses:
            for course in [coidmap[coid]] + list(coidmap[coid].and_):
                for c in in_relationship_with:
                    course.or_.add(
                        [coidmap[c]] + list(coidmap[c].and_)
                    )
        # FIXME puts it out of order, does this matter?

@db_session
def populateCoreList(program: md.Program):
    # Every core
    for data in sr.fetchCores(program.poid):
        populateCore(*data, program)

    db.commit()


def populateDB():
    with db_session:
        populateProgramList()

        # Process every program
        for program in md.Program.select():
            print(program.name)
            populateCoreList(program)  # populate list of cores

        db.commit()

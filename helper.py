from pony.orm.core import db_session

import db_inter.models as md
import yaml


# Stupid and innefficeint dont care TODO
# Get math scores
@db_session
def getMath():
    with open("score.yaml") as b:
        data = yaml.safe_load(b)

    math = {}
    for c in md.Course.select().fetch():
        for s in data['math'].keys():
            a = c.name.lower().split()
            b = s.split()
            if a[0] == b[0] and a[1] == b[1]:
                math[c.id] = data['math'][s]
    return math

@db_session
def getPrograms():
    programs = []
    for program in md.Program.select().fetch():
        programs.append(program.to_dict())
    return programs


def getSetCourseIDs(set):
    a = set.order_by(1).fetch()
    ids = []
    for i in a:
        ids.append(i.id)
    return ids


def setToList(set, callback=None):
    e = set.order_by(1).fetch()
    return e


@db_session
def processCourse(course, seen_course={}):
    # course = None, nonconforming course has been passed
    if course and not seen_course.get(course.id):
        d = course.to_dict()
        seen_course[course.id] = d

        d['requisites'] = []
        for req in setToList(course.requisites):
            d['requisites'].append(
                processRequisite(req, seen_course)
            )
        return d


def processRequisite(req, seen_course):
    def getids(set):
        a = set.order_by(1).fetch()
        ids = []
        for i in a:
            ids.append(i.course.coid)
        return ids

    d = req.to_dict()
    d['and_'] = getids(req.and_)
    d['or_'] = getids(req.or_)

    processCourse(
        req.req_course, seen_course
    )
    return d


def getCoreOptions(core, seen_course):
    options = {}
    for cc in setToList(core.courses):
        d = cc.to_dict()
        d['and_'] = getSetCourseIDs(cc.and_)
        d['or_'] = getSetCourseIDs(cc.or_)

        id = d['id']
        d.pop('id', None)

        options[id] = d

        processCourse(cc.course, seen_course)

    return options


@db_session
def getProgram(id_):
    out = {
        'course': {},
        'core': [],
        'program': {}
    }

    # Get cores
    program = md.Program.select().where(id=id_).fetch()[0]
    out["program"]['poid'] = program.poid
    out["program"]['name'] = program.name

    cores = program.cores.order_by(md.Core.core_id).fetch()
    # result_list=[]
    for core in cores:
        out['core'].append(
            {
                "core_id": core.core_id,
                "name": core.name,
                'courses': getCoreOptions(core, out['course'])
                # FIXME evil? idk, making this all a class seems more evil.
            }
        )
    # print(out['course'])

    return out

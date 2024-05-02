from pony.orm import Required, Set, Optional
import json
from . import db


def setToJSON(set, ctx):
    e = set.order_by(1).fetch()
    return [cc.toJSON(ctx) for cc in e]


def getids(set):
    a = set.order_by(1).fetch()
    ids = []
    for i in a:
        ids.append(i.course.coid)
    return ids


class Program(db.Entity):
    name = Required(str)
    poid = Required(int, unique=True)

    required_by = Set("Requisite", reverse="req_program")

    cores = Set("Core", reverse="program")


class Core(db.Entity):
    name = Required(str)
    core_id = Required(str, unique=True)

    program = Required(Program, reverse="cores")

    courses = Set("CoreCourse", reverse="core")

    def toJSON(self, ctx):
        d = self.to_dict()

        d['courses'] = setToJSON(self.courses, ctx)

        return d


class Course(db.Entity):
    name = Optional(str)
    coid = Required(int, unique=True)
    description = Optional(str)

    required_by = Set("Requisite", reverse="req_course")
    requisites = Set("Requisite", reverse="course")

    core_courses = Set("CoreCourse", reverse="course")

    def toJSON(self, ctx):
        d = self.to_dict()

        d['requisites'] = setToJSON(self.requisites, ctx)
        return d


class CoreCourse(db.Entity):
    core = Set(Core, reverse="courses")
    course = Optional(Course)

    nonconforming = Optional(str)

    and_ = Set("CoreCourse", reverse="and_")
    or_ = Set("CoreCourse", reverse="or_")

    def getName(self):
        """
        Returns either course name or nonconforming text

        :return: str
        """

        if self.course:
            return self.course.name
        else:
            return self.nonconforming

    def toJSON(self, ctx):
        d = self.to_dict()

        ctx['course'].append(self.course.toJSON(ctx))

        d['and_'] = getids(self.and_)
        d['or_'] = getids(self.or_)
        return d


class Requisite(db.Entity):
    course = Required(Course, reverse="requisites")
    req_course = Optional(Course, reverse="required_by")
    req_program = Optional(Program, reverse="required_by")  # insane edge case

    type_ = Required(str)

    and_ = Set("Requisite", reverse="and_")
    or_ = Set("Requisite", reverse="or_")

    def toJSON(self, ctx):
        d = self.to_dict()
        d['and_'] = getids(self.and_)
        d['or_'] = getids(self.or_)
        return d

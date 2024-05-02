from pony.orm import Database

db = Database()
# TODO connector

from .models import * # import models

# db.bind(provider='sqlite', filename='data4.sqlite', create_db=True)
# # db.bind(provider='sqlite', filename=':memory:', create_db=True)
# db.generate_mapping(create_tables=True)

# __all__ = [
#     'corelist', 'course', 'programlist'
# ]

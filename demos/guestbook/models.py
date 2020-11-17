""" ``models`` module.
"""

from datetime import datetime


class Greeting(object):
    def __init__(self, id=0, created_on=None, author="", message=""):
        self.id = id
        self.created_on = created_on or datetime.now()
        self.author = author
        self.message = message

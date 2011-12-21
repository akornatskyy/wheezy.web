"""
"""

from wheezy.core.comp import u


class Credential(object):
    def __init__(self, username=u(''), password=u('')):
        self.username = username
        self.password = password

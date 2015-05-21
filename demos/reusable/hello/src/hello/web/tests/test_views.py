import unittest

from wheezy.http.functional import WSGIClient

from app import main


path_for = main.options['path_for']


class HelloTestCase(unittest.TestCase):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        self.client = None

    def path_for(self, name, **kwargs):
        return '/' + path_for('hello:' + name, **kwargs)

    def test_welcome(self):
        assert 200 == self.client.get(self.path_for('welcome'))
        assert 'Hello World!' in self.client.content

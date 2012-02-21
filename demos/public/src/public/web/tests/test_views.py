
""" ``test_views`` module.
"""

import unittest

from wheezy.http.functional import WSGIClient

from app import main


class PublicTestCase(unittest.TestCase):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_home(self):
        """ Ensure home page is rendered.
        """
        assert 200 == self.client.get('/en/home')
        assert '- Home</title>' in self.client.content

    def test_about(self):
        """ Ensure about page is rendered.
        """
        assert 200 == self.client.get('/en/about')
        assert '- About</title>' in self.client.content

    def test_widgets(self):
        """ Ensure widgets page is rendered.
        """
        assert 200 == self.client.get('/en/widgets')
        assert '- Widgets</title>' in self.client.content
        assert 'no error</b>' in self.client.content

    def test_widgets_with_errors(self):
        """ Ensure widgets-with-errors page is rendered.
        """
        assert 200 == self.client.get('/en/widgets-with-errors')
        assert '- Widgets</title>' in self.client.content
        assert 'error reported</b>' in self.client.content

    def test_static_files(self):
        """ Ensure static content is served.
        """
        for static_file in [
                '/favicon.ico',
                '/static/css/site.css',
                '/static/js/core.js',
                '/static/js/autocomplete.js',
                '/static/js/jquery-1.7.1.min.js',
                ]:
            assert 200 == self.client.get(static_file)

    def test_static_file_not_found(self):
        """ Ensure 404 status code for non existing
            static content.
        """
        self.client.get('/static/css/unknown.css')
        assert 404 == self.client.follow()

    def test_static_file_forbidden(self):
        """ Ensure 403 status code for forbidden
            static content.
        """
        self.client.get('/static/js/')
        assert 403 == self.client.follow()

    def test_static_file_gzip(self):
        """
        """
        self.client.get('/static/css/site.css', environ={
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate'
        })
        assert 'gzip' in self.client.headers['Content-Encoding']

    def test_head_static_file(self):
        """
        """
        assert 200 == self.client.head('/static/css/site.css')
        assert 0 == len(self.client.content)

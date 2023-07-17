""" ``test_views`` module.
"""

import re
import unittest

try:
    import json
except ImportError:  # pragma: nocover
    json = None  # noqa

from app import main
from config import template_engine
from wheezy.http.functional import WSGIClient

if template_engine.startswith("wheezy"):
    re_ws = re.compile(r" \s+", re.MULTILINE)

    def extra_whitespace(s):
        return re_ws.search(s)

else:

    def extra_whitespace(s):
        return False


class PublicTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_root(self):
        """Ensure root page is rendered."""
        assert 200 == self.client.get("/")
        assert "- Home</title>" in self.client.content

    def test_home(self):
        """Ensure home page is rendered."""
        assert 200 == self.client.get("/en/home")
        assert "- Home</title>" in self.client.content

    def test_about(self):
        """Ensure about page is rendered."""
        assert 200 == self.client.get("/en/about")
        assert "- About</title>" in self.client.content

    def test_space_around_newline(self):
        """space around newline in markup should not be removed"""
        self.client.get("/en/home")
        assert re.search(r"elit\.\s+Donec", self.client.content)
        assert re.search(r"enim,\s+quis", self.client.content)
        assert not re.search('"type', self.client.content)

    def test_extra_whitespace(self):
        for url in ["/", "/en/home", "/en/about"]:
            assert 200 == self.client.get(url)
            assert not extra_whitespace(self.client.content)


class StaticFilesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_static_files(self):
        """Ensure static content is served."""
        for static_file in [
            "/favicon.ico",
            "/static/css/site.css",
            "/static/img/error.png",
            "/static/js/core.js",
            "/static/js/autocomplete.js",
            "/static/js/jquery-1.7.1.min.js",
        ]:
            assert 200 == self.client.get(static_file)

    def test_static_file_not_found(self):
        """Ensure 404 status code for non existing
        static content.
        """
        assert 302 == self.client.get("/static/css/unknown.css")
        assert "404" in self.client.headers["Location"][0]

    def test_static_file_forbidden(self):
        """Ensure 403 status code for forbidden
        static content.
        """
        assert 302 == self.client.get("/static/../templates/")
        assert "403" in self.client.headers["Location"][0]

    def test_static_file_gzip(self):
        """Ensure static files are compressed."""
        self.client.get(
            "/static/css/site.css",
            environ={
                "SERVER_PROTOCOL": "HTTP/1.1",
                "HTTP_ACCEPT_ENCODING": "gzip, deflate",
            },
        )
        assert "gzip" in self.client.headers["Content-Encoding"]

    def test_static_file_if_modified_since(self):
        """Request static resource with If-Modified-Since header."""
        assert 200 == self.client.get("/static/css/site.css")
        last_modified = self.client.headers["Last-Modified"][0]
        assert 304 == self.client.get(
            "/static/css/site.css",
            environ={"HTTP_IF_MODIFIED_SINCE": last_modified},
        )

    def test_static_file_if_none_match(self):
        """Request static resource with If-None-Match header."""
        assert 200 == self.client.get("/static/css/site.css")
        etag = self.client.headers["ETag"][0]
        assert 304 == self.client.get(
            "/static/css/site.css", environ={"HTTP_IF_NONE_MATCH": etag}
        )

    def test_head_static_file(self):
        """Request static resource with HTTP HEAD."""
        assert 200 == self.client.head("/static/css/site.css")
        assert 0 == len(self.client.content)


class ErrorTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_error_400(self):
        """Ensure bad request page is rendered."""
        assert 400 == self.client.get("/en/error/400")
        assert "Code 400" in self.client.content

    def test_error_403(self):
        """Ensure forbidden page is rendered."""
        assert 403 == self.client.get("/en/error/403")
        assert "Code 403" in self.client.content

    def test_error_404(self):
        """Ensure not found page is rendered."""
        assert 404 == self.client.get("/en/error/404")
        assert "Code 404" in self.client.content

    def test_route_not_found(self):
        """Ensure not found page is rendered."""
        self.client.get("/test-not-found")
        assert 404 == self.client.follow()
        assert "Code 404" in self.client.content

    def test_error_500(self):
        """Ensure internal error page is rendered."""
        assert 500 == self.client.get("/en/error/500")
        assert "Code 500" in self.client.content

    def test_space_around_newline(self):
        """space around newline in markup should not be removed"""
        self.client.get("/en/error/404")
        r = re.compile(r"been\s+removed")
        assert r.search(self.client.content)

    def test_extra_whitespace(self):
        for url in [
            "/en/error/400",
            "/en/error/403",
            "/en/error/404",
            "/en/error/500",
        ]:
            self.client.get(url)
            assert not extra_whitespace(self.client.content)

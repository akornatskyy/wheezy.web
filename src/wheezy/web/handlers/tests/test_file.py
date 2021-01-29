""" Unit tests for ``wheezy.web.handlers.base``.
"""

import os.path
import unittest
from unittest.mock import Mock

from wheezy.web.handlers.file import FileHandler, file_handler
from wheezy.web.handlers.method import handler_factory

rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class FileHandlerTestCase(unittest.TestCase):
    """Test the ``FileHandler``."""

    def setUp(self):
        self.options = {}
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.route_args = {}
        self.mock_request.environ = {"route_args": self.route_args}
        self.mock_request.root_path = "my_site/"
        self.handler = handler_factory(
            FileHandler, self.mock_request, root=rootdir
        )

    def test_get_out_of_root_path(self):
        """if requested file is not within root directory
        respond with HTTP forbidden.
        """
        self.route_args["path"] = "../forbidden.txt"
        response = self.handler.get()
        assert 403 == response.status_code

    def test_get_not_found(self):
        """Requested file not found, respond with HTTP not found."""
        self.route_args["path"] = "not_found.txt"
        response = self.handler.get()
        assert 404 == response.status_code

    def test_get_not_a_file(self):
        """Requested path is valid but it is not a file."""
        self.route_args["path"] = "tests"
        response = self.handler.get()
        assert 403 == response.status_code

    def test_get_file(self):
        """Requested path is valid."""
        self.route_args["path"] = "tests/test_file.py"
        response = self.handler.get()
        assert 200 == response.status_code
        assert "text/x-python" == response.content_type
        assert response.encoding is None

    def test_head(self):
        """Requested with HTTP HEAD method."""
        self.route_args["path"] = "tests/test_file.py"
        response = self.handler.head()
        assert 200 == response.status_code
        assert not response.buffer


class FileHandlerFactoryTestCase(unittest.TestCase):
    """Test the ``file_handler``."""

    def setUp(self):
        self.options = {}
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.route_args = {}
        self.mock_request.method = "GET"
        self.mock_request.environ = {"route_args": self.route_args}
        self.mock_request.root_path = "my_site/"

    def test_get(self):
        """get."""
        self.route_args["path"] = "tests/test_file.py"
        response = file_handler(rootdir)(self.mock_request)
        assert 200 == response.status_code

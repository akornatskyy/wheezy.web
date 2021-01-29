""" Unit tests for ``wheezy.web.middleware.errors``.
"""

import unittest
from unittest.mock import Mock

from wheezy.web.transforms import handler_transforms


class HandlerTransformsTestCase(unittest.TestCase):
    """Test the ``handler_transforms``."""

    def test_single_strategy(self):
        """A single transform supplied.

        @transforms(gzip)
        get(self):
            ...
        """

        def transform(request, response):
            assert "request" == request
            return response + "-transformed"

        mock_handler = Mock()
        mock_handler.request = "request"
        mock_handler_method = Mock(return_value="response")
        handler = handler_transforms(transform)(mock_handler_method)
        assert "response-transformed" == handler(mock_handler)

    def test_multiple_strategy(self):
        """A multiple transforms supplied.

        @transforms(minimize, gzip)
        get(self):
            ...
        """

        def transform_a(request, response):
            assert "request" == request
            return response + "-A"

        def transform_b(request, response):
            assert "request" == request
            return response + "-B"

        mock_handler = Mock()
        mock_handler.request = "request"
        mock_handler_method = Mock(return_value="response")
        handler = handler_transforms(transform_a, transform_b)(
            mock_handler_method
        )
        assert "response-A-B" == handler(mock_handler)

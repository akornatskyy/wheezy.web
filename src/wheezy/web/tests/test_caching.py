
""" Unit tests for ``wheezy.web.caching``.
"""

import unittest

from mock import Mock


class HandlerCacheTestCase(unittest.TestCase):
    """ Test the ``handler_cache``.
    """

    def test_profile_not_enabled(self):
        """ Cache profile is disabled.
        """
        from wheezy.web.caching import handler_cache
        mock_profile = Mock()
        mock_profile.enabled = False
        mock_method = Mock(return_value='response')
        handler = handler_cache(mock_profile)(mock_method)
        assert 'response' == handler('handler')

    def test_no_cache(self):
        """ No cache strategy, cache policy is defined in response
            do not overwrite.
        """
        from wheezy.web.caching import handler_cache
        mock_profile = Mock()
        mock_profile.enabled = True
        mock_profile.request_vary = None
        mock_response = Mock()
        mock_response.cache_policy = 'policy'
        mock_method = Mock(return_value=mock_response)
        handler = handler_cache(mock_profile)(mock_method)
        assert mock_response == handler('handler')
        assert 'policy' == mock_response.cache_policy
        mock_method.assert_called_once_with('handler')

    def test_no_cache_apply_cache_policy(self):
        """ No cache strategy, cache policy is not defined in response,
            apply cache policy per cache profile.
        """
        from wheezy.web.caching import handler_cache
        mock_profile = Mock()
        mock_profile.enabled = True
        mock_profile.request_vary = None
        mock_profile.cache_policy.return_value = 'policy'
        mock_response = Mock()
        mock_response.cache_policy = None
        mock_method = Mock(return_value=mock_response)
        handler = handler_cache(mock_profile)(mock_method)
        assert mock_response == handler('handler')
        assert 'policy' == mock_response.cache_policy
        mock_method.assert_called_once_with('handler')

    def test_cache(self):
        """ Cache strategy, cache policy is defined in response
            do not overwrite.
        """
        from wheezy.web.caching import handler_cache
        mock_profile = Mock()
        mock_profile.enabled = True
        mock_profile.request_vary = 'vary'
        mock_response = Mock()
        mock_response.cache_profile = 'profile'
        mock_response.cache_policy = 'policy'
        mock_method = Mock(return_value=mock_response)
        handler = handler_cache(mock_profile)(mock_method)
        assert mock_response == handler('handler')
        assert 'policy' == mock_response.cache_policy
        mock_method.assert_called_once_with('handler')
        assert mock_profile == mock_response.cache_profile

    def test_cache_apply_cache_policy(self):
        """ Cache strategy, cache policy is not defined in response,
            apply cache policy per cache profile.
        """
        from wheezy.web.caching import handler_cache
        mock_profile = Mock()
        mock_profile.enabled = True
        mock_profile.request_vary = 'vary'
        mock_profile.cache_policy.return_value = 'policy'
        mock_response = Mock()
        mock_response.cache_profile = 'profile'
        mock_response.cache_policy = None
        mock_method = Mock(return_value=mock_response)
        handler = handler_cache(mock_profile)(mock_method)
        assert mock_response == handler('handler')
        assert 'policy' == mock_response.cache_policy
        mock_method.assert_called_once_with('handler')
        assert mock_profile == mock_response.cache_profile

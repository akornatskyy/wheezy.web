
""" Unit tests for ``wheezy.web.handlers.base``.
"""

import unittest

from mock import Mock
from mock import patch


class BaseHandlerTestCase(unittest.TestCase):
    """ Test the ``BaseHandler``.
    """

    def setUp(self):
        from wheezy.core.url import urlparts
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {
            'AUTH_COOKIE': '_a',
            'AUTH_COOKIE_PATH': 'members',
            'AUTH_COOKIE_DOMAIN': 'python.org',
            'AUTH_COOKIE_SECURE': True,
            'HTTP_COOKIE_SECURE': False,
            'HTTP_COOKIE_HTTPONLY': False,
            'translations_manager': {'en': 'translations'}
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {'locale': 'en'}}
        self.mock_request.method = 'GET'
        self.mock_request.root_path = 'my_site/'
        self.mock_request.cookies = {}
        self.mock_request.urlparts = urlparts(
            scheme='https', netloc='python.org')
        self.handler = handler_factory(BaseHandler, self.mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_context(self):
        """ context
        """
        context = self.handler.context
        assert ('errors', 'locale', 'principal', 'translations') \
            == tuple(sorted(context.keys()))


class BaseHandlerRoutingTestCase(unittest.TestCase):
    """ Test the ``BaseHandler`` routing.
    """

    def setUp(self):
        from wheezy.core.url import urlparts
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {}
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.mock_request.method = 'GET'
        self.mock_request.root_path = 'my_site/'
        self.mock_request.urlparts = urlparts(
            scheme='https', netloc='python.org')
        self.handler = handler_factory(BaseHandler, self.mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_path_for(self):
        """ path_for.
        """
        mock_path_for = Mock(return_value='welcome')
        self.options['path_for'] = mock_path_for

        assert 'my_site/welcome' == self.handler.path_for('default')
        mock_path_for.assert_called_once_with('default')

    def test_absolute_url_for(self):
        """ absolute_url_for.
        """
        mock_path_for = Mock(return_value='welcome')
        self.options['path_for'] = mock_path_for

        url = self.handler.absolute_url_for('default')
        assert 'https://python.org/my_site/welcome' == url
        mock_path_for.assert_called_once_with('default')

    def test_redirect_and_see_other(self):
        """ redirect_for and see_other: non-ajax request.
        """
        mock_path_for = Mock(return_value='welcome')
        self.options['path_for'] = mock_path_for
        self.mock_request.ajax = False

        response = self.handler.redirect_for('default')
        assert 302 == response.status_code
        url = response.headers[-1][1]
        assert 'https://python.org/my_site/welcome' == url

        response = self.handler.see_other_for('default')
        assert 303 == response.status_code
        url = response.headers[-1][1]
        assert 'https://python.org/my_site/welcome' == url

    def test_ajax_redirect_see_other(self):
        """ redirect_for and see_other_fori: ajax request.
        """
        mock_path_for = Mock(return_value='welcome')
        self.options['path_for'] = mock_path_for
        self.mock_request.ajax = True

        response = self.handler.redirect_for('default')
        assert 207 == response.status_code
        url = response.headers[-1][1]
        assert 'https://python.org/my_site/welcome' == url

        response = self.handler.see_other_for('default')
        assert 207 == response.status_code
        url = response.headers[-1][1]
        assert 'https://python.org/my_site/welcome' == url


class BaseHandlerI18NTestCase(unittest.TestCase):
    """ Test the ``BaseHandler`` i18n.
    """

    def setUp(self):
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {}
        mock_request = Mock()
        mock_request.options = self.options
        mock_request.environ = {'route_args': {}}
        self.handler = handler_factory(BaseHandler, mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_locale(self):
        """ Ensure default implemenation takes locale from route_args.
        """
        self.handler.route_args['locale'] = 'en'
        assert 'en' == self.handler.locale

    def test_no_locale(self):
        """ Ensure default implemenation takes locale from route_args.
        """
        assert '' == self.handler.locale

    def test_translations(self):
        """ Translations returned per current locale.
        """
        translations_manager = {
            'en': 'en-trans',
            'uk': 'uk-trans'
        }
        self.handler.route_args['locale'] = 'uk'
        self.options['translations_manager'] = translations_manager
        assert 'uk-trans' == self.handler.translations

    def test_translation(self):
        """ By default null_translation returned. Classes drived
            from BaseHandler must override this property.
        """
        from wheezy.core.i18n import null_translations
        assert null_translations == self.handler.translation

    def test_gettext(self):
        """ gettext.
        """
        assert 'x' == self.handler.gettext('x')

    def test_gettext2(self):
        """ _.
        """
        assert 'x' == self.handler._('x')


class BaseHandlerModelsTestCase(unittest.TestCase):
    """ Test the ``BaseHandler`` models.
    """

    def setUp(self):
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {}
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.handler = handler_factory(BaseHandler, self.mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_errors(self):
        """ errors is an empty dict.
        """
        assert {} == self.handler.errors

    def test_try_update_model(self):
        """ try_update_model
        """
        from wheezy.core.i18n import null_translations
        translations_manager = {
            'en': {
                'validation': null_translations
            }
        }
        self.handler.route_args['locale'] = 'en'
        self.options['translations_manager'] = translations_manager
        self.mock_request.form = {
            'name': ['test']
        }
        model = {
            'name': ''
        }
        assert self.handler.try_update_model(model)
        assert 'test' == model['name']


class BaseHandlerTemplatesTestCase(unittest.TestCase):
    """ Test the ``BaseHandler`` templates.
    """

    def setUp(self):
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {
            'AUTH_COOKIE': '_a'
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {'locale': 'en'}}
        self.mock_request.root_path = 'my_site/'
        self.mock_request.cookies = {}
        self.handler = handler_factory(BaseHandler, self.mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_helpers(self):
        """ template helpers.
        """
        assert (
            '_', 'absolute_url_for', 'errors', 'locale', 'path_for',
            'principal', 'resubmission', 'route_args', 'xsrf'
        ) == tuple(sorted(self.handler.helpers.keys()))

    def test_render_template(self):
        """ render_template.
        """
        mock_render_template = Mock(return_value='html')
        self.options['render_template'] = mock_render_template
        assert 'html' == self.handler.render_template('signin.html')
        assert mock_render_template.called

    def test_render_template_with_kwargs(self):
        """ render_template with optional data arguments.
        """
        def render_template(template_name, data):
            assert 'signin.html' == template_name
            assert 10 == data['test']
            return 'html'
        self.options['render_template'] = render_template
        assert 'html' == self.handler.render_template(
            'signin.html', test=10)

    def test_render_response(self):
        """ render_response.
        """
        mock_render_template = Mock(return_value='html')
        self.options.update({
            'render_template': mock_render_template,
            'CONTENT_TYPE': 'text/plain',
            'ENCODING': 'UTF-8'
        })
        response = self.handler.render_response('signin.html')
        assert mock_render_template.called
        assert 200 == response.status_code
        assert 'text/plain' == response.content_type

    def test_json_response(self):
        """ json_response.
        """
        from wheezy.web.handlers import base
        self.options.update({
            'ENCODING': 'UTF-8'
        })
        patcher = patch.object(base, 'json_response')
        mock_json_response = patcher.start()
        mock_json_response.return_value = 'response'

        assert 'response' == self.handler.json_response({})

        patcher.stop()
        mock_json_response.assert_called_once_with({}, 'UTF-8')


class BaseHandlerAuthenticationTestCase(unittest.TestCase):
    """ Test the ``BaseHandler`` authentication.
    """

    def setUp(self):
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {
            'AUTH_COOKIE': '_a',
            'AUTH_COOKIE_PATH': 'members',
            'AUTH_COOKIE_DOMAIN': 'python.org',
            'AUTH_COOKIE_SECURE': True,
            'HTTP_COOKIE_SECURE': False,
            'HTTP_COOKIE_HTTPONLY': False
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.mock_request.root_path = 'my_site/'
        self.mock_request.cookies = {}
        self.handler = handler_factory(BaseHandler, self.mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_getprincipal_auth_cookie_not_available(self):
        """ auth cookie has not been supplied in request.
        """
        assert self.handler.getprincipal() is None

    def test_getprincipal_auth_cookie_expired(self):
        """ auth cookie has been expired.
        """
        self.mock_request.cookies['_a'] = 'x'
        mock_ticket = Mock()
        mock_ticket.decode.return_value = (None, None)
        self.options['ticket'] = mock_ticket

        assert self.handler.getprincipal() is None
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_a' == cookie.name
        assert 'my_site/members' == cookie.path
        assert 'python.org' == cookie.domain

    def test_getprincipal_renew_ticket(self):
        """ ticket decoded but needs renewal.
        """
        self.mock_request.cookies['_a'] = 'x'
        mock_ticket = Mock()
        mock_ticket.max_age = 100
        mock_ticket.decode.return_value = ('15747\x1f\x1f\x1f', 40)
        mock_ticket.encode.return_value = 'encrypted'
        self.options['ticket'] = mock_ticket

        principal = self.handler.getprincipal()
        assert '15747' == principal.id
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_a' == cookie.name
        assert 'encrypted' == cookie.value
        assert 'my_site/members' == cookie.path
        assert 'python.org' == cookie.domain

    def test_getprincipal_valid_ticket(self):
        """ ticket decoded.
        """
        self.mock_request.cookies['_a'] = 'x'
        mock_ticket = Mock()
        mock_ticket.max_age = 100
        mock_ticket.decode.return_value = ('15747\x1f\x1f\x1f', 80)
        self.options['ticket'] = mock_ticket

        principal = self.handler.getprincipal()
        assert '15747' == principal.id
        assert not self.handler.cookies
        assert principal == self.handler.principal


class BaseHandlerXSRFTestCase(unittest.TestCase):
    """ Test the ``BaseHandler`` XSRF.
    """

    def setUp(self):
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {
            'XSRF_NAME': '_x'
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.mock_request.root_path = 'my_site/'
        self.mock_request.cookies = {}
        self.handler = handler_factory(BaseHandler, self.mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_getxsrf_cookie_not_available(self):
        """ XSRF cookie was not supplied with request.
        """
        from wheezy.web.handlers import base
        self.options.update({
            'HTTP_COOKIE_DOMAIN': None,
            'HTTP_COOKIE_SECURE': True
        })
        patcher = patch.object(base, 'shrink_uuid')
        mock_shrink_uuid = patcher.start()
        mock_shrink_uuid.return_value = 'xsrf'
        assert 'xsrf' == self.handler.getxsrf_token()
        patcher.stop()
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_x' == cookie.name
        assert 'xsrf' == cookie.value

    def test_getxsrf_cookie(self):
        """ XSRF cookie was not supplied with request.
        """
        self.mock_request.cookies['_x'] = 'xsrf'
        assert 'xsrf' == self.handler.getxsrf_token()
        assert 'xsrf' == self.handler.xsrf_token

    def test_del_xsrf_cookie(self):
        """ delxsrf_token.
        """
        self.options.update({
            'HTTP_COOKIE_DOMAIN': None,
            'HTTP_COOKIE_SECURE': True,
            'HTTP_COOKIE_HTTPONLY': True
        })
        self.handler.delxsrf_token()
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_x' == cookie.name

    def test_validate_xsrf_token_not_in_form(self):
        """ validate_xsrf_token but it is missing in form
            submitted.
        """
        self.options.update({
            'HTTP_COOKIE_DOMAIN': None,
            'HTTP_COOKIE_SECURE': True,
            'HTTP_COOKIE_HTTPONLY': True
        })
        self.mock_request.form = {}
        assert not self.handler.validate_xsrf_token()
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_x' == cookie.name
        assert cookie.value is None

    def test_validate_xsrf_token_no_match(self):
        """ form token does not match cookie value.
        """
        self.mock_request.cookies['_x'] = 'pK8vVOmIT1y_1jUceSmbdA'
        self.mock_request.form = {'_x': ['x']}
        assert not self.handler.validate_xsrf_token()

    def test_validate_xsrf_token_invalid_uuid(self):
        """ validate_xsrf_token there is match but it is not valid
            uuid value.
        """
        self.mock_request.cookies['_x'] = 'x'
        self.mock_request.form = {'_x': ['x']}
        assert not self.handler.validate_xsrf_token()

    def test_validate_xsrf_token(self):
        """ validate_xsrf_token.
        """
        self.mock_request.cookies['_x'] = 'pK8vVOmIT1y_1jUceSmbdA'
        self.mock_request.form = {'_x': ['pK8vVOmIT1y_1jUceSmbdA']}
        assert self.handler.validate_xsrf_token()

    def test_xsrf_widget(self):
        """ xsrf_widget.
        """
        self.mock_request.cookies['_x'] = 'xsrf'
        widget = self.handler.xsrf_widget()
        assert '<input type="hidden" name="_x" value="xsrf" />' == widget


class BaseHandlerResibmissionTestCase(unittest.TestCase):
    """ Test the ``BaseHandler`` resubmission.
    """

    def setUp(self):
        from wheezy.web.handlers.base import BaseHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {
            'RESUBMISSION_NAME': '_r'
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.mock_request.root_path = 'my_site/'
        self.mock_request.cookies = {}
        self.handler = handler_factory(BaseHandler, self.mock_request)
        assert isinstance(self.handler, BaseHandler)

    def test_getresubmission_not_supplied(self):
        """ XSRF cookie was not supplied with request.
        """
        self.options.update({
            'HTTP_COOKIE_DOMAIN': None,
            'HTTP_COOKIE_SECURE': True,
            'HTTP_COOKIE_HTTPONLY': True
        })
        assert '0' == self.handler.getresubmission()
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_r' == cookie.name
        assert '0' == cookie.value

    def test_getresubmission(self):
        """ XSRF cookie supplied with request.
        """
        self.mock_request.cookies['_r'] = '100'
        assert '100' == self.handler.getresubmission()
        assert '100' == self.handler.resubmission

    def test_delresubmission(self):
        """ delete resubmission cookie.
        """
        self.options.update({
            'HTTP_COOKIE_DOMAIN': None,
            'HTTP_COOKIE_SECURE': True,
            'HTTP_COOKIE_HTTPONLY': True
        })
        self.mock_request.cookies['_r'] = '100'
        self.handler.delresubmission()
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_r' == cookie.name
        assert cookie.value is None

    def test_validate_resubmission_ajax(self):
        """ validate_resubmission in ajax request.
        """
        self.mock_request.ajax = True
        self.mock_request.cookies['_r'] = '123'
        self.mock_request.form = {'_r': ['123']}
        assert self.handler.validate_resubmission()

    def test_validate_resubmission_form_value_missing(self):
        """ form value is missing.
        """
        self.mock_request.ajax = False
        self.mock_request.form = {}
        assert not self.handler.validate_resubmission()

    def test_validate_resubmission_no_match(self):
        """ form value does not match one in cookie.
        """
        self.mock_request.ajax = False
        self.mock_request.cookies['_r'] = '2'
        self.mock_request.form = {'_r': ['1']}
        assert not self.handler.validate_resubmission()

    def test_validate_resubmission_counter_not_int(self):
        """ counter is not valid integer value.
        """
        self.options.update({
            'HTTP_COOKIE_DOMAIN': None,
            'HTTP_COOKIE_SECURE': True,
            'HTTP_COOKIE_HTTPONLY': True
        })
        self.mock_request.ajax = False
        self.mock_request.cookies['_r'] = 'x'
        self.mock_request.form = {'_r': ['x']}
        assert not self.handler.validate_resubmission()
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_r' == cookie.name
        assert '0' == cookie.value

    def test_validate_resubmission(self):
        """ validate_resubmission.
        """
        self.options.update({
            'HTTP_COOKIE_DOMAIN': None,
            'HTTP_COOKIE_SECURE': True,
            'HTTP_COOKIE_HTTPONLY': True
        })
        self.mock_request.ajax = False
        self.mock_request.cookies['_r'] = '247'
        self.mock_request.form = {'_r': ['247']}
        assert self.handler.validate_resubmission()
        assert 1 == len(self.handler.cookies)
        cookie = self.handler.cookies[0]
        assert '_r' == cookie.name
        assert '248' == cookie.value

    def test_resubmission_widget(self):
        """ resubmission_widget.
        """
        self.mock_request.ajax = False
        self.mock_request.cookies['_r'] = '123'
        widget = self.handler.resubmission_widget()
        assert '<input type="hidden" name="_r" value="123" />' == widget

    def test_resubmission_ajax(self):
        """ resubmission_widget in ajax request.
        """
        self.mock_request.ajax = True
        self.mock_request.cookies['_r'] = '123'
        widget = self.handler.resubmission_widget()
        assert '' == widget


class RedirectRouteHandlerTestCase(unittest.TestCase):
    """ Test the ``RedirectRouteHandler``.
    """

    def setUp(self):
        from wheezy.core.url import urlparts
        from wheezy.web.handlers.base import RedirectRouteHandler
        from wheezy.web.handlers.method import handler_factory
        mock_path_for = Mock(return_value='welcome')
        self.options = {'path_for': mock_path_for}
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.mock_request.method = 'GET'
        self.mock_request.root_path = 'my_site/'
        self.mock_request.urlparts = urlparts(
            scheme='https', netloc='python.org')
        self.handler = handler_factory(
            RedirectRouteHandler,
            self.mock_request,
            'default')
        assert isinstance(self.handler, RedirectRouteHandler)

    def test_redirect_http_get(self):
        """ get.
        """
        self.mock_request.ajax = False
        response = self.handler.get()
        assert 302 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]

    def test_redirect_http_get_ajax(self):
        """ get in ajax request.
        """
        self.mock_request.ajax = True
        response = self.handler.get()
        assert 207 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]

    def test_redirect_http_post(self):
        """ post.
        """
        self.mock_request.ajax = False
        response = self.handler.post()
        assert 302 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]

    def test_redirect_http_post_ajax(self):
        """ post in ajax request.
        """
        self.mock_request.ajax = True
        response = self.handler.post()
        assert 207 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]


class RedirectHandlerTestCase(unittest.TestCase):
    """ Test the ``redirect_handler``.
    """

    def setUp(self):
        from wheezy.core.url import urlparts
        mock_path_for = Mock(return_value='welcome')
        self.options = {'path_for': mock_path_for}
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.mock_request.ajax = False
        self.mock_request.root_path = 'my_site/'
        self.mock_request.urlparts = urlparts(
            scheme='https', netloc='python.org')

    def test_redirect_http_get(self):
        """ get.
        """
        from wheezy.web.handlers.base import redirect_handler
        self.mock_request.method = 'GET'
        response = redirect_handler('welcome')(self.mock_request)
        assert 302 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]

    def test_redirect_http_post(self):
        """ post.
        """
        from wheezy.web.handlers.base import redirect_handler
        self.mock_request.method = 'POST'
        response = redirect_handler('welcome')(self.mock_request)
        assert 302 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]


class PermanentRedirectHandlerTestCase(unittest.TestCase):
    """ Test the ``permanent_redirect_handler``.
    """

    def setUp(self):
        from wheezy.core.url import urlparts
        mock_path_for = Mock(return_value='welcome')
        self.options = {'path_for': mock_path_for}
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.mock_request.environ = {'route_args': {}}
        self.mock_request.ajax = False
        self.mock_request.root_path = 'my_site/'
        self.mock_request.urlparts = urlparts(
            scheme='https', netloc='python.org')

    def test_redirect_http_get(self):
        """ get.
        """
        from wheezy.web.handlers.base import permanent_redirect_handler
        self.mock_request.method = 'GET'
        response = permanent_redirect_handler('welcome')(self.mock_request)
        assert 301 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]

    def test_redirect_http_post(self):
        """ post.
        """
        from wheezy.web.handlers.base import permanent_redirect_handler
        self.mock_request.method = 'POST'
        response = permanent_redirect_handler('welcome')(self.mock_request)
        assert 301 == response.status_code
        assert 'https://python.org/my_site/welcome' == response.headers[-1][1]

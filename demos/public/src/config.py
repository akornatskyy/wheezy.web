"""
"""

from wheezy.caching.memory import MemoryCache
from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.security.crypto.ticket import Ticket
from wheezy.web.templates import MakoTemplate

from membership.repository.mock import MockFactory


cache = MemoryCache()

# Custom
options = {
        'membership': MockFactory,
        'membership_cache': cache,
}

# HTTPErrorMiddleware
options.update({
        'http_errors': defaultdict(lambda: 'http500', {
            # HTTP status code: route name
            400: 'http400',
            403: 'http403',
            404: 'http404',
            500: 'http500',
        }),
})

# BaseHandler
options.update({
        'translations_manager': TranslationsManager(
            directories=['i18n'],
            default_lang='en'),

        'render_template': MakoTemplate(
            directories=['content/templates'],
            filesystem_checks=False),

        'ticket': Ticket(
            max_age=1200,
            salt='JNbCog95cDTo1NRb7inP',
            options={
                'CRYPTO_ENCRYPTION_KEY': '4oqiKhW3qzP2EiattMt7',
                'CRYPTO_VALIDATION_KEY': 'A7GfjxIBCBA3vNqvafWf'
            }),

        'AUTH_COOKIE': '_a',
        'AUTH_COOKIE_DOMAIN': None,
        'AUTH_COOKIE_PATH': '',
        'AUTH_COOKIE_SECURE': False,

        'XSRF_NAME': '_x',
        'RESUBMISSION_NAME': '_c'
})

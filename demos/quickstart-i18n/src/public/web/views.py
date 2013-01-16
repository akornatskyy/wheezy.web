"""
"""

from datetime import timedelta

from wheezy.core.descriptors import attribute
from wheezy.http import response_cache
from wheezy.http.transforms import gzip_transform
from wheezy.http.transforms import response_transforms
from wheezy.web.handlers import BaseHandler
from wheezy.web.handlers import file_handler
from wheezy.web.handlers import template_handler

from public.web.profile import public_cache_profile
from public.web.profile import static_cache_profile


class PublicHandler(BaseHandler):
    """ Anything common for public area handlers goes here.
    """

    @attribute
    def translation(self):
        return self.translations['public']


class WelcomeHandler(PublicHandler):

    @response_cache(public_cache_profile)
    @response_transforms(gzip_transform())
    def get(self):
        # There are two entry points for this handler:
        # one that respond to / and the other one with
        # locale in path, e.g. /en. Stick with default
        # route so menu locate properly reverse url for
        # current route.
        self.route_args['route_name'] = 'default'
        return self.render_response('public/home.html')


wraps_handler = lambda p: lambda h: response_cache(p)(
    response_transforms(gzip_transform(compress_level=9))(h))

extra = {
    'translation_name': 'public'
}

#w = wraps_handler(public_cache_profile, **extra)
#home = w(template_handler('public/home.html'))

# cached by nginx
http400 = template_handler('public/http400.html', status_code=400, **extra)
http403 = template_handler('public/http403.html', status_code=403, **extra)
http404 = template_handler('public/http404.html', status_code=404, **extra)
http500 = template_handler('public/http500.html', status_code=500, **extra)

w = wraps_handler(static_cache_profile)
static_file = w(file_handler(root='content/static/', age=timedelta(hours=1)))

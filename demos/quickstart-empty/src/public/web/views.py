"""
"""

import os.path

from config import root_dir
from public.web.profile import public_cache_profile, static_cache_profile
from wheezy.http import response_cache
from wheezy.http.transforms import gzip_transform, response_transforms

from wheezy.web.handlers import BaseHandler, file_handler, template_handler
from wheezy.web.transforms import handler_transforms


class WelcomeHandler(BaseHandler):
    @response_cache(public_cache_profile)
    @handler_transforms(gzip_transform())
    def get(self):
        return self.render_response("public/home.html")


def wraps_handler(p):
    def wrapper(h):
        return response_cache(p)(
            response_transforms(gzip_transform(compress_level=9))(h)
        )

    return wrapper


# w = wraps_handler(public_cache_profile)
# home = w(template_handler('public/home.html'))

# cached by nginx
http400 = template_handler("public/http400.html", status_code=400)
http403 = template_handler("public/http403.html", status_code=403)
http404 = template_handler("public/http404.html", status_code=404)
http500 = template_handler("public/http500.html", status_code=500)

w = wraps_handler(static_cache_profile)
static_file = w(file_handler(os.path.join(root_dir, "content/static/")))

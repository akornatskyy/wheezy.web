"""
"""

from wheezy.web.handlers.base import BaseHandler


class SignInHandler(BaseHandler):

    def get(self):
        return self.render_response('membership/signin.html')

class SignUpHandler(BaseHandler):

    def get(self):
        return self.render_response('membership/signup.html')

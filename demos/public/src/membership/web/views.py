"""
"""

from wheezy.core.collections import attrdict
from wheezy.core.comp import u
from wheezy.core.descriptors import attribute
from wheezy.web.handlers.base import BaseHandler

from membership.models import Credential
from membership.service.factory import Factory
from membership.validation import credential_validator


class SignInHandler(BaseHandler):

    @attribute
    def viewdata(self):
        return attrdict({
            'remember_me': False
            })

    @attribute
    def factory(self):
        return Factory(self.context)

    def get(self, credential=None):
        credential = credential or Credential()
        return self.render_response('membership/signin.html',
                credential=credential,
                viewdata=self.viewdata)

    def post(self):
        credential = Credential()
        if (not self.try_update_model(credential)
                & self.try_update_model(self.viewdata)
                or not self.validate(credential, credential_validator)
                or not self.factory.membership.authenticate(credential)):
            credential.password = u('')
            return self.get(credential)
        return self.redirect_for('home')


class SignUpHandler(BaseHandler):

    def get(self):
        return self.render_response('membership/signup.html')

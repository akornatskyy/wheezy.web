"""
"""

from operator import itemgetter

from wheezy.core.collections import attrdict
from wheezy.core.comp import u
from wheezy.core.descriptors import attribute
from wheezy.http import bad_request
from wheezy.security import Principal
from wheezy.web.caching import handler_cache
from wheezy.web.handlers import BaseHandler

from config import none_cache_profile
from membership.models import Credential
from membership.models import Registration
from membership.service.factory import Factory
from membership.validation import credential_validator
from membership.validation import password_match_validator
from membership.validation import registration_validator


class SignInHandler(BaseHandler):

    @attribute
    def model(self):
        return attrdict({
            'remember_me': False
            })

    @attribute
    def translation(self):
        return self.translations['membership']

    @attribute
    def factory(self):
        return Factory(self.context)

    @handler_cache(profile=none_cache_profile)
    def get(self, credential=None):
        if self.principal:
            return self.redirect_for('default')
        credential = credential or Credential()
        return self.render_response('membership/signin.html',
                credential=credential,
                model=self.model)

    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)
        credential = Credential()
        if (not self.try_update_model(credential)
                & self.try_update_model(self.model)
                or not self.validate(credential, credential_validator)
                or not self.factory.membership.authenticate(credential)):
            credential.password = u('')
            return self.get(credential)
        self.principal = Principal(
                id=credential.username,
                alias=credential.username)
        del self.xsrf_token
        return self.redirect_for('default')


class SignOutHandler(BaseHandler):

    def get(self):
        del self.principal
        return self.redirect_for('default')


class SignUpHandler(BaseHandler):

    @attribute
    def model(self):
        return attrdict({
            'password': u(''),
            'confirm_password': u(''),
            'questionid': '1'
            })

    @attribute
    def translation(self):
        return self.translations['membership']

    @attribute
    def factory(self):
        return Factory(self.context)

    @handler_cache(profile=none_cache_profile)
    def get(self, registration=None):
        if self.principal:
            return self.redirect_for('default')
        registration = registration or Registration()
        return self.render_response('membership/signup.html',
                registration=registration,
                credential=registration.credential,
                account=registration.account,
                model=self.model,
                questions=sorted(
                    self.factory.membership.password_questions.items(),
                    key=itemgetter(1))
                )

    def post(self):
        if not self.validate_resubmission():
            self.error('Your registration request has been queued. '
                    'Please wait while your request will be processed. '
                    'If your request fails please try again.')
            return self.get()
        registration = Registration()
        if (not self.try_update_model(self.model)
                & self.try_update_model(registration)
                & self.try_update_model(registration.account)
                & self.try_update_model(registration.credential)
                or not self.validate(self.model, password_match_validator)
                & self.validate(registration, registration_validator)
                or not self.factory.membership.create_account(registration)):
            registration.credential.password = u('')
            self.model.confirm_password = u('')
            return self.get(registration)
        self.principal = Principal(
                id=registration.credential.username,
                alias=registration.credential.username)
        del self.resubmission
        return self.redirect_for('default')

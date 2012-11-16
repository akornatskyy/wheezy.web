"""
"""

from wheezy.core.collections import attrdict
from wheezy.core.comp import u
from wheezy.core.descriptors import attribute
from wheezy.http import none_cache_profile
from wheezy.security import Principal
from wheezy.web import handler_cache
from wheezy.web.handlers import BaseHandler

from factory import Factory
from membership.models import Credential
from membership.models import Registration
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
        return self.render_response(
            'membership/signin.html',
            credential=credential,
            model=self.model)

    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)
        credential = Credential()
        if (not self.try_update_model(credential)
                & self.try_update_model(self.model)
                or not self.validate(credential, credential_validator)
                or not self.authenticate(credential)):
            if self.request.ajax:
                return self.json_response({'errors': self.errors})
            credential.password = u('')
            return self.get(credential)
        self.principal = Principal(
            id=credential.username,
            alias=credential.username,
            roles=tuple(self.factory.membership.roles(
                credential.username)))
        del self.xsrf_token
        return self.see_other_for('default')

    def authenticate(self, credential):
        #with self.factory as f:
        f = self.factory.__enter__()
        try:
            return f.membership.authenticate(credential)
        finally:
            f.__exit__(None, None, None)


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

    def factory(self, session_name):
        return Factory(self.context, session_name)

    @handler_cache(profile=none_cache_profile)
    def get(self, registration=None):
        if self.principal:
            return self.redirect_for('default')
        registration = registration or Registration()

        #with self.factory('ro') as f:
        f = self.factory('ro')
        try:
            f.__enter__()
            questions = f.membership.list_password_questions
            account_types = f.membership.list_account_types
        finally:
            f.__exit__(None, None, None)

        return self.render_response(
            'membership/signup.html',
            model=self.model,
            registration=registration,
            account=registration.account,
            credential=registration.credential,
            questions=questions,
            account_types=account_types)

    def post(self):
        if not self.validate_resubmission():
            self.error(self._('Your registration request has been queued. '
                              'Please wait while your request will be '
                              'processed. If your request fails please '
                              'try again.'))
            return self.get()
        registration = Registration()
        if (not self.try_update_model(self.model)
                & self.try_update_model(registration)
                & self.try_update_model(registration.account)
                & self.try_update_model(registration.credential)
                or not self.validate(self.model, password_match_validator)
                & self.validate(registration, registration_validator)
                or not self.create_account(registration)):
            if self.request.ajax:
                return self.json_response({'errors': self.errors})
            registration.credential.password = u('')
            self.model.confirm_password = u('')
            return self.get(registration)

        #with self.factory('ro') as f:
        f = self.factory('ro')
        try:
            f.__enter__()
            roles = f.membership.roles(registration.credential.username)
        finally:
            f.__exit__(None, None, None)

        self.principal = Principal(
            id=registration.credential.username,
            alias=registration.account.display_name,
            roles=roles)
        del self.resubmission
        return self.see_other_for('default')

    def create_account(self, registration):
        #with self.factory('rw') as f:
        f = self.factory('rw')
        try:
            f.__enter__()
            succeed = f.membership.create_account(registration)
            f.session.commit()
            return succeed
        finally:
            f.__exit__(None, None, None)

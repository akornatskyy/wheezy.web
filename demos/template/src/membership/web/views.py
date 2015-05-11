"""
"""

from datetime import datetime
from time import time

from wheezy.core.collections import attrdict
from wheezy.core.comp import u
from wheezy.core.descriptors import attribute
from wheezy.http import none_cache_profile
from wheezy.security import Principal
from wheezy.web import handler_cache
from wheezy.web.handlers import BaseHandler

from factory import Factory
from lockout import locker
from lockout import signin_alert
from membership.models import Credential
from membership.models import Registration
from membership.models import account_types
from membership.validation import credential_validator
from membership.validation import password_match_validator
from membership.validation import registration_validator


class MembershipBaseHandler(BaseHandler):

    @attribute
    def translation(self):
        return self.translations['membership']

    def factory(self, session_name='ro'):
        return Factory(session_name, **self.context)


class SignInHandler(MembershipBaseHandler):

    lockout = locker.define(
        name='signin attempts',
        by_ip=dict(count=3, duration=60, alert=signin_alert)
    )

    @attribute
    def model(self):
        return attrdict({
            'username': u(''),
            'remember_me': False
        })

    @handler_cache(profile=none_cache_profile)
    def get(self, credential=None):
        if self.principal:
            return self.redirect_for('default')
        credential = credential or Credential()
        return self.render_response(
            'membership/signin.html',
            credential=credential,
            model=self.model)

    @lockout.forbid_locked
    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)
        credential = Credential()
        if (not self.try_update_model(credential) &
                self.try_update_model(self.model) or
                not self.validate(credential, credential_validator) or
                not self.authenticate(credential)):
            if self.request.ajax:
                return self.json_response({'errors': self.errors})
            credential.password = u('')
            return self.get(credential)
        del self.xsrf_token
        return self.see_other_for('default')

    @lockout.guard
    def authenticate(self, credential):
        # with self.factory('ro') as f:
        f = self.factory('ro').__enter__()
        try:
            if not f.membership.authenticate(credential):
                return False
            roles = f.membership.roles(credential.username)
        finally:
            f.__exit__(None, None, None)
        self.principal = Principal(
            id=credential.username,
            roles=roles,
            alias=credential.username)
        if self.model.remember_me:
            # The above code appends authentication cookie of type session
            # to the list of self.cookies, we set expries to make
            # it persistent. Once renewed turns back to session, otherwise
            # override setprincipal.
            self.cookies[-1].expires = datetime.utcfromtimestamp(
                time() + self.ticket.max_age)
        return True


class SignOutHandler(BaseHandler):

    def get(self):
        del self.principal
        return self.redirect_for('default')


class SignUpHandler(MembershipBaseHandler):

    lockout = locker.define(
        name='signup attempts',
        by_ip=dict(count=2, duration=60)
    )

    @attribute
    def model(self):
        return attrdict({
            'password': u(''),
            'confirm_password': u(''),
            'question_id': '1'
        })

    @handler_cache(profile=none_cache_profile)
    def get(self, registration=None):
        if self.principal:
            return self.redirect_for('default')
        registration = registration or Registration()

        # with self.factory('ro') as f:
        f = self.factory('ro')
        try:
            f.__enter__()
            questions = f.membership.list_password_questions
        finally:
            f.__exit__(None, None, None)

        return self.render_response(
            'membership/signup.html',
            model=self.model,
            registration=registration,
            account=registration.account,
            credential=registration.credential,
            questions=questions,
            account_types=tuple((k, self.gettext(v))
                                for k, v in account_types))

    @lockout.forbid_locked
    def post(self):
        if not self.validate_resubmission():
            self.error(self._('Your registration request has been queued. '
                              'Please wait while your request will be '
                              'processed. If your request fails please '
                              'try again.'))
            return self.get()
        registration = Registration()
        if (not self.try_update_model(self.model) &
                self.try_update_model(registration) &
                self.try_update_model(registration.account) &
                self.try_update_model(registration.credential) or
                not self.validate(self.model, password_match_validator) &
                self.validate(registration, registration_validator) or
                not self.create_account(registration)):
            if self.request.ajax:
                return self.json_response({'errors': self.errors})
            registration.credential.password = u('')
            self.model.confirm_password = u('')
            return self.get(registration)

        # with self.factory('ro') as f:
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

    @lockout.quota
    def create_account(self, registration):
        # with self.factory('rw') as f:
        f = self.factory('rw')
        try:
            f.__enter__()
            succeed = f.membership.create_account(registration)
            f.session.commit()
            return succeed
        finally:
            f.__exit__(None, None, None)

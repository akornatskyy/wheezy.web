"""
"""

from datetime import datetime

from wheezy.core.collections import attrdict
from wheezy.core.descriptors import attribute
from wheezy.http import bad_request
from wheezy.web.handlers import BaseHandler
from wheezy.web.handlers import template_handler


home = template_handler('public/home.html')
about = template_handler('public/about.html')


class NowHandler(BaseHandler):

    def get(self):
        if not self.request.ajax:
            return bad_request()
        return self.json_response({'now': datetime.now()})


class WidgetsHandler(BaseHandler):

    @attribute
    def model(self):
        return attrdict({
            'username': 'John Smith',
            'username_status': 'Taken!',
            'password': '',
            'password_status': '',
            'notes': 'Lorem ipsum dolor sit amet.',
            'pref': 'abc',
            'prefs': ['ab', 'c'],
            'remember_me': True,
            'scm': 'hg',
            'scms': ['git', 'hg']
            })

    @attribute
    def translation(self):
        return self.translations['membership']

    def get(self):
        if 'errors' == self.route_args.mode:
            self.error('Error Message')
            for k in self.model.keys():
                self.errors[k] = ['Error Message A', 'Error Message B']
        return self.render_response('public/widgets.html',
                        model=self.model,
                        message='Your changes have been saved.',
                        scm=[('git', 'Git'),
                            ('hg', 'Mercurial'),
                            ('svn', 'SVN')])

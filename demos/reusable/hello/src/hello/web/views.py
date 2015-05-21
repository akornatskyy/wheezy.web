from wheezy.web.handlers import BaseHandler

from factory import Factory


class HelloBaseHandler(BaseHandler):

    def factory(self, session_name='ro'):
        return Factory(session_name, **self.context)


class WelcomeHandler(HelloBaseHandler):

    def get(self):
        msg = self.say_hi()
        return self.render_response('hello/welcome.html', msg=msg)

    def say_hi(self):
        # with self.factory('ro') as f:
        f = self.factory('ro').__enter__()
        try:
            msg = f.hello.say_hi('World')
        finally:
            f.__exit__(None, None, None)
        return msg

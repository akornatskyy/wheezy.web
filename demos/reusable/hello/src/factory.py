from hello.factory import HelloFactoryMixin
from wheezy.core.db import NullSession


class Factory(HelloFactoryMixin):
    def __init__(self, session_name, **context):
        self.context = context
        self.session = sessions[session_name]()
        self.factory = None

    def __enter__(self):
        self.session.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.__exit__(exc_value, exc_value, traceback)


sessions = {"ro": NullSession, "rw": NullSession}

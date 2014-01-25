"""
"""

from config import config


class Factory(object):

    def __init__(self, session_name, **context):
        self.context = context
        self.session = sessions[session_name]()
        self.factory = RepositoryFactory(self.session)

    def __enter__(self):
        self.session.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.__exit__(exc_value, exc_value, traceback)


class RepositoryFactory(object):

    def __init__(self, session):
        self.session = session


def mock_sessions():
    from wheezy.core.db import NullSession
    return {
        'ro': NullSession, 'rw': NullSession
    }


# region: configuration details
mode = config.get('runtime', 'mode')
if mode == 'mock':
    sessions = mock_sessions()
else:
    raise NotImplementedError(mode)
del mode, config

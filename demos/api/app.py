"""
"""

from datetime import timedelta

from wheezy.caching import MemoryCache
from wheezy.caching.patterns import Cached
from wheezy.core.collections import attrdict
from wheezy.core.comp import u
from wheezy.core.db import NullSession
from wheezy.core.descriptors import attribute
from wheezy.http import CacheProfile
from wheezy.http import WSGIApplication
from wheezy.http import response_cache
from wheezy.http.cache import etag_md5crc32
from wheezy.http.middleware import http_cache_middleware_factory
from wheezy.http.response import HTTPResponse
from wheezy.http.response import bad_request
from wheezy.http.response import method_not_allowed
from wheezy.http.response import not_found
from wheezy.http.transforms import gzip_transform
from wheezy.routing import url
from wheezy.validation import Validator
from wheezy.validation.mixin import ErrorsMixin
from wheezy.validation.rules import and_
from wheezy.validation.rules import int_adapter
from wheezy.validation.rules import length
from wheezy.validation.rules import must
from wheezy.validation.rules import range
from wheezy.validation.rules import required
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory
from wheezy.web.transforms import handler_transforms


# region: foundation

class APIHandler(BaseHandler):

    def __call__(self):
        method = self.request.method
        if method == 'GET':
            return self.get()
        elif method == 'POST':
            return self.post()
        elif method == 'PUT':
            return self.put()
        elif method == 'DELETE':
            return self.delete()
        return method_not_allowed()

    def put(self):
        return method_not_allowed()

    def delete(self):
        return method_not_allowed()

    def factory(self, session_name):
        return Factory(session_name, self.context)

    def status_response(self):
        assert not self.errors
        response = HTTPResponse('application/json; charset=UTF-8', 'UTF-8')
        response.write_bytes('{"status":"OK"}')
        return response

    def error_response(self, status_code=200):
        response = self.json_response({'errors': self.errors})
        response.status_code = status_code
        return response


def accept_json(**kwargs):
    supported = kwargs['keys']
    assert isinstance(supported, frozenset)

    def decorate(handler):
        def wraps(self):
            if 'application/json' not in self.request.content_type:
                return bad_request()
            unexpected = frozenset(self.request.form.keys()) - supported
            if unexpected:
                self.error('Unexpected keys: %s' % ', '.join(unexpected))
                return self.error_response(status_code=400)
            return handler(self)
        return wraps
    return decorate


# region: config

cache = MemoryCache()
cached = Cached(cache, time=timedelta(hours=4))


# region: models

def Task(other={}):
    return attrdict({
        'task_id': None,
        'title': u(''),
        'status': 1
    }, **other)

Task.keys = frozenset(Task().keys())


# region: cache profiles

task_cache_profile = CacheProfile(
    'both',
    duration=timedelta(hours=2),
    # this cause browser to send request each time
    # so the server is able to respond with code 304
    http_max_age=0,
    vary_environ=['HTTP_ACCEPT_ENCODING'],
    etag_func=etag_md5crc32,
    enabled=True)


# region: cache dependency keys

class keys(object):

    @staticmethod
    def task_list():
        return 'tals:'

    @staticmethod
    def task(task_id):
        return 'tage:' + task_id + ':'


# region: web handlers

class TaskListHandler(APIHandler):

    @response_cache(profile=task_cache_profile)
    @handler_transforms(gzip_transform())
    def get(self):
        with self.factory('ro') as f:
            tasks = f.api.search_tasks()
        response = self.json_response({'tasks': tasks})
        response.cache_dependency = (keys.task_list(),)
        return response

    @accept_json(keys=Task.keys)
    def post(self):
        task = Task(self.request.form)
        if (not self.validate(task, task_validator) or
                not self.add_task(task)):
            return self.error_response()
        response = self.json_response({'task': {'task_id': task.task_id}})
        response.status_code = 201
        return response

    # region: internal details

    def add_task(self, task):
        task.task_id = None
        with self.factory('rw') as f:
            if not f.api.save_task(task):
                return False
            f.session.commit()
        cached.dependency.delete(keys.task_list())
        return True


class TaskHandler(APIHandler):

    @response_cache(profile=task_cache_profile)
    @handler_transforms(gzip_transform())
    def get(self):
        with self.factory('ro') as f:
            task = f.api.get_task(self.route_args.task_id)
        if not task:
            return not_found()
        response = self.json_response({'task': task})
        response.cache_dependency = (keys.task(task.task_id),)
        return response

    @accept_json(keys=Task.keys)
    def put(self):
        with self.factory('ro') as f:
            task = f.api.get_task(self.route_args.task_id)
        if not task:
            return not_found()
        task.update(self.request.form)
        if (not self.validate(task, task_validator) or
                not self.update_task(task)):
            return self.error_response()
        return self.status_response()

    def delete(self):
        if not self.remove_task(self.route_args.task_id):
            return not_found()
        return self.status_response()

    # region: internal details

    def update_task(self, task):
        task.task_id = self.route_args.task_id
        with self.factory('rw') as f:
            if not f.api.save_task(task):
                return False
            f.session.commit()
        cached.dependency.delete_multi((
            keys.task_list(), keys.task(task.task_id)))
        return True

    def remove_task(self, task_id):
        with self.factory('rw') as f:
            if not f.api.remove_task(task_id):
                return False
            f.session.commit()
        cached.dependency.delete_multi((
            keys.task_list(), keys.task(task_id)))
        return True


# region: service

class APIService(ErrorsMixin):

    def __init__(self, errors):
        self.errors = errors

    def search_tasks(self):
        return [t for t in sorted(tasks.values(), key=lambda m: m.task_id)]

    def get_task(self, task_id):
        return tasks.get(task_id)

    def save_task(self, task):
        if not task.task_id:
            task.task_id = str(int(max(tasks, key=lambda k: int(k))) + 1)
        elif task.task_id not in tasks:
            self.error('Not Found.')
            return False
        tasks[task.task_id] = task
        return True

    def remove_task(self, task_id):
        if task_id not in tasks:
            self.error('Not Found.')
            return False
        del tasks[task_id]
        return True


# region: samples

tasks = {
    '1': attrdict(task_id='1', title='Task #1', status=1),
    '2': attrdict(task_id='2', title='Task #2', status=2),
    '3': attrdict(task_id='3', title='Task #3', status=1)
}


# region: factory

class Factory(object):

    def __init__(self, session_name, context):
        self.context = context
        self.session = sessions[session_name]()

    def __enter__(self):
        self.session.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.__exit__(exc_value, exc_value, traceback)

    @attribute
    def api(self):
        return APIService(self.context['errors'])


sessions = {'ro': NullSession, 'rw': NullSession}


# region: rules

int_type = and_(int_adapter(must(lambda i: True)),
                must(lambda s: isinstance(s, int),
                     message_template='Requires int type.'))

# region: validation

task_validator = Validator({
    'title': [required, length(min=4), length(max=250)],
    'status': [required, int_type, range(min=1), range(max=3)]
})


# region: urls

api_v1_urls = [
    url('tasks', TaskListHandler),
    url('task/{task_id:number}', TaskHandler)
]

all_urls = [
    url('api/v1/', api_v1_urls)
]


# region: config

options = {
    'http_cache': cache
}

# region: app

main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        http_cache_middleware_factory,
        path_routing_middleware_factory
    ],
    options=options
)


if __name__ == '__main__':
    from wsgiref.handlers import BaseHandler
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        BaseHandler.http_version = '1.1'
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')

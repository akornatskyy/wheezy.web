"""
"""

import unittest

from wheezy.core.comp import json_dumps
from wheezy.http.functional import WSGIClient

from app import main


# region: foundation


class WSGIAPIClient(WSGIClient):

    def json_post(self, path, params):
        return self.go(path, 'POST', content_type='application/json',
                       content=json_dumps(params))

    def json_put(self, path, params):
        return self.go(path, 'PUT', content_type='application/json',
                       content=json_dumps(params))

    def json_delete(self, path):
        return self.go(path, 'DELETE')


# region: mixins

class TaskMixin(object):

    def list_task(self):
        assert 200 == self.client.get(self.path_for('task_list'))
        return self.client.json

    def get_task(self, task_id):
        if 200 != self.client.get(
                self.path_for('task', task_id=task_id)):
            return None
        return self.client.json

    def add_task(self, task):
        if 201 != self.client.json_post(
                self.path_for('task_list'), task):
            return None
        return self.client.json

    def update_task(self, task):
        if 200 != self.client.json_put(
                self.path_for('task', task_id=task['task_id']), task):
            return None
        return self.client.json

    def remove_task(self, task_id):
        if 200 != self.client.json_delete(
                self.path_for('task', task_id=task_id)):
            return None
        return self.client.json


# region: test cases

class APITestCase(unittest.TestCase, TaskMixin):

    def setUp(self):
        self.client = WSGIAPIClient(main)
        self.path_for = main.options['path_for']

    def test_list(self):
        r = self.list_task()
        assert r and r.tasks

    def test_get_not_found(self):
        assert not self.get_task(task_id='0')
        assert 404 == self.client.status_code
        assert not self.get_task(task_id='x')
        assert 404 == self.client.status_code

    def test_get(self):
        r = self.get_task(task_id='1')
        assert r and r.task

    def test_add_bad_request(self):
        assert not self.add_task({'x': ''})
        assert 400 == self.client.status_code

    def test_add_validation_erros(self):
        assert not self.add_task({'title': ''})
        assert 200 == self.client.status_code
        assert 'errors' in self.client.json

    def test_add(self):
        r = self.add_task({'title': 'Test'})
        task_id = r.task.task_id
        r = self.list_task()
        assert task_id in [t.task_id for t in r.tasks]

    def test_update_bad_request(self):
        assert not self.update_task({'task_id': '1', 'x': ''})
        assert 400 == self.client.status_code

    def test_update_not_found(self):
        assert not self.update_task({'task_id': '0'})
        assert 404 == self.client.status_code

    def test_update_validation_errors(self):
        assert self.update_task({'task_id': '1', 'title': ''})
        assert 'errors' in self.client.json

    def test_update(self):
        r = self.update_task({'task_id': '1', 'title': 'Test'})
        assert r and 'errors' not in r
        r = self.get_task(task_id='1')
        assert 'Test' == r.task.title
        r = self.list_task()
        assert 'Test' in [t.title for t in r.tasks]

    def test_delete_not_found(self):
        assert not self.remove_task(task_id='0')
        assert 404 == self.client.status_code

    def test_delete(self):
        r = self.add_task({'title': 'Test'})
        r = self.remove_task(r.task.task_id)
        assert r and 'errors' not in r

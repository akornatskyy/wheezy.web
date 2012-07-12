
""" ``benchmark_views`` module.
"""

from wheezy.core.benchmark import Benchmark

from public.web.tests.test_views import PublicTestCase
from public.web.tests.test_views import ErrorTestCase


class PublicBenchmarkTestCase(PublicTestCase, ErrorTestCase):

    def runTest(self):
        """ Perform bachmark and print results.
        """
        b = Benchmark((
            self.test_root,
            self.test_home,
            self.test_about,
            self.test_error_400,
            self.test_error_403,
            self.test_error_404,
        ), 1000)
        b.report('public', baselines={
            'test_root': 1.0,
            'test_home': 0.8,
            'test_about': 0.8,
            'test_error_400': 0.75,
            'test_error_403': 0.75,
            'test_error_404': 0.75,
        })


class StaticFilesBenchmarkTestCase(PublicTestCase, ErrorTestCase):

    def runTest(self):
        """ Perform bachmark and print results.
        """
        b = Benchmark((
            self.test_static_files,
            self.test_static_file_not_found,
            self.test_static_file_forbidden,
            self.test_static_file_gzip,
            self.test_head_static_file,
        ), 1000)
        b.report('static', baselines={
            'test_static_files': 1.00,
            'test_static_file_not_found': 0.95,
            'test_static_file_forbidden': 1.05,
            'test_static_file_gzip': 5.2,
            'test_head_static_file': 5.6,
        })

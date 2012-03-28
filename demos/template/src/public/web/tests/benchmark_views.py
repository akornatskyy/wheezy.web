
""" ``benchmark_views`` module.
"""

from wheezy.core.benchmark import Benchmark

from public.web.tests.test_views import PublicTestCase
from public.web.tests.test_views import ErrorTestCase


class BenchmarkTestCase(PublicTestCase, ErrorTestCase):  # pragma: nocover

    def runTest(self):
        """ Perform bachmark and print results.
        """
        p = Benchmark((
            self.test_home,
            self.test_about,
            self.test_error_400,
            self.test_error_403,
            self.test_error_404,
            self.test_static_files,
            self.test_static_file_not_found,
            self.test_static_file_forbidden,
            self.test_static_file_gzip,
            self.test_head_static_file,
            ), 1000)
        p.report('public', baselines={
                'test_home': 1.0,
                'test_about': 0.95,
                'test_error_400': 0.95,
                'test_error_403': 0.95,
                'test_error_404': 0.95,
                'test_static_files': 2.17,
                'test_static_file_not_found': 2.1,
                'test_static_file_forbidden': 2.3,
                'test_static_file_gzip': 11.4,
                'test_head_static_file': 12.5,
        })

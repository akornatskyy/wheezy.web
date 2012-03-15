
""" ``benchmark_views`` module.
"""

from wheezy.core.benchmark import Benchmark

from public.web.tests.test_views import PublicTestCase


class BenchmarkTestCase(PublicTestCase):

    def runTest(self):
        """ Perform bachmark and print results.
        """
        p = Benchmark((
            self.test_home,
            self.test_about,
            self.test_now,
            self.test_widgets,
            self.test_widgets_with_errors,
            self.test_static_files,
            self.test_static_file_not_found,
            self.test_static_file_forbidden,
            self.test_static_file_if_modified_since,
            self.test_static_file_if_none_match,
            self.test_static_file_gzip,
            self.test_head_static_file
            ), 1000)
        p.report('public', baselines={
                'test_home': 1.0,
                'test_about': 0.89,
                'test_now': 3.34,
                'test_widgets': 0.52,
                'test_widgets_with_errors': 0.51,
                'test_static_files': 1.655,
                'test_static_file_not_found': 2.0,
                'test_static_file_forbidden': 2.2,
                'test_static_file_if_modified_since': 7.0,
                'test_static_file_if_none_match': 11.3,
                'test_static_file_gzip': 8.91,
                'test_head_static_file': 9.08
        })

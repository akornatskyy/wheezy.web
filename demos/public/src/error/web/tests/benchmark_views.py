
""" ``benchmark_views`` module.
"""

from wheezy.core.benchmark import Benchmark

from error.web.tests.test_views import ErrorTestCase


class BenchmarkTestCase(ErrorTestCase):

    def runTest(self):
        """ Perform bachmark and print results.
        """
        p = Benchmark((
            self.test_error_400,
            self.test_error_403,
            self.test_error_404,
            ), 1000)
        p.report('error', baselines={
                'test_error_400': 1.0,
                'test_error_403': 1.0,
                'test_error_404': 1.0,
        })

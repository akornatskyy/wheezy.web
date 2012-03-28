
""" ``benchmark_views`` module.
"""

from wheezy.core.benchmark import Benchmark

from membership.web.tests.test_views import MembershipTestCase


class BenchmarkTestCase(MembershipTestCase):  # pragma: nocover

    def runTest(self):
        """ Perform bachmark and print results.
        """
        p = Benchmark((
            self.test_signin,
            self.test_signup,
            self.test_signout,
            ), 1000)
        p.report('membership', baselines={
                'test_signin': 1.0,
                'test_signup': 0.89,
                'test_signout': 4.32,
        })


""" ``benchmark_views`` module.
"""

from wheezy.core.benchmark import Benchmark

from membership.web.tests.test_views import MembershipTestCase
from membership.web.tests.test_views import SignInTestCase
from membership.web.tests.test_views import SignUpTestCase


class MembershipBenchmarkTestCase(MembershipTestCase):

    def runTest(self):
        """ Perform benchmark and print results.
        """
        b = Benchmark((
            self.test_signin,
            self.test_signup,
            self.test_signout,
        ), 1000)
        b.report('membership', baselines={
            'test_signin': 1.0,
            'test_signup': 0.89,
            'test_signout': 4.32,
        })


class SigninBenchmarkTestCase(SignInTestCase):

    def runTest(self):
        """ Perform benchmark and print results.
        """
        b = Benchmark((
            self.test_validation_error,
            self.test_unknown_user,
            self.test_xrsf_token_invalid
        ), 200)
        b.report('signin', baselines={
            'test_validation_error': 1.0,
            'test_unknown_user': 1.0,
            'test_xrsf_token_invalid': 0.94
        })


class SignupBenchmarkTestCase(SignUpTestCase):

    def runTest(self):
        """ Perform benchmark and print results.
        """
        b = Benchmark((
            self.test_validation_error,
            self.test_already_registered,
            self.test_resubmission_token_invalid,
        ), 100)
        b.report('signup', baselines={
            'test_validation_error': 1.0,
            'test_already_registered': 1.0,
            'test_resubmission_token_invalid': 1.05
        })


""" ``benchmark_views`` module.
"""

from wheezy.core.benchmark import Benchmark

from membership.web.tests.test_views import MembershipTestCase
from membership.web.tests.test_views import SignInTestCase
from membership.web.tests.test_views import SignUpTestCase


class BenchmarkMembershipTestCase(MembershipTestCase):

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
                'test_signup': 0.667,
                'test_signout': 3.62,
        })


class BenchmarkSigninTestCase(SignInTestCase):

    def runTest(self):
        """ Perform bachmark and print results.
        """
        p = Benchmark((
            self.test_validation_error,
            self.test_unknown_user,
            self.test_xrsf_token_invalid
            ), 200)
        p.report('signin', baselines={
                'test_validation_error': 1.0,
                'test_unknown_user': 1.0,
                'test_xrsf_token_invalid': 0.94
        })


class BenchmarkSignupTestCase(SignUpTestCase):

    def runTest(self):
        """ Perform bachmark and print results.
        """
        p = Benchmark((
            self.test_validation_error,
            self.test_already_registered,
            self.test_resubmission_token_invalid,
            ), 100)
        p.report('signup', baselines={
                'test_validation_error': 1.0,
                'test_already_registered': 1.0,
                'test_resubmission_token_invalid': 1.05
        })

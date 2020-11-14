""" ``benchmark_views`` module.
"""

from membership.web.tests.test_views import (
    MembershipTestCase,
    SignInTestCase,
    SignUpTestCase,
)
from wheezy.core.json import json_encode
from wheezy.http.functional import BenchmarkMixin

try:
    json_encode({})
    has_json = True
except NotImplementedError:
    has_json = False


class MembershipBenchmarkTestCase(MembershipTestCase, BenchmarkMixin):
    def test_benchmark(self):
        """Perform benchmark and print results."""
        b = self.benchmark(
            (
                self.test_signin,
                self.test_signup,
                self.test_signout,
            ),
            1000,
        )
        b.report(
            "membership",
            baselines={
                "test_signin": 1.0,
                "test_signup": 0.89,
                "test_signout": 4.32,
            },
        )


class SigninBenchmarkTestCase(SignInTestCase, BenchmarkMixin):
    def test_benchmark(self):
        """Perform benchmark and print results."""
        b = self.benchmark(
            [self.test_validation_errors, self.test_xrsf_token_invalid], 200
        )
        b.report(
            "signin",
            baselines={
                "test_validation_errors": 1.0,
                "test_xrsf_token_invalid": 0.94,
            },
        )


class SignupBenchmarkTestCase(SignUpTestCase, BenchmarkMixin):
    def test_benchmark(self):
        """Perform benchmark and print results."""
        b = self.benchmark(
            [
                self.test_validation_errors,
                self.test_already_registered,
                self.test_resubmission_token_invalid,
            ],
            100,
        )
        b.report(
            "signup",
            baselines={
                "test_validation_error": 1.0,
                "test_already_registered": 1.0,
                "test_resubmission_token_invalid": 1.05,
            },
        )


try:
    from membership.web.tests.test_views import (
        SignInAJAXTestCase,
        SignUpAJAXTestCase,
    )

    class SigninAJAXBenchmarkTestCase(SignInAJAXTestCase, BenchmarkMixin):
        def test_benchmark(self):
            """Perform benchmark and print results."""
            b = self.benchmark(
                [
                    self.test_ajax_validation_errors,
                    self.test_ajax_xrsf_token_invalid,
                ],
                200,
            )
            b.report(
                "ajax-signin",
                baselines={
                    "test_ajax_validation_errors": 1.0,
                    "test_ajax_xrsf_token_invalid": 0.94,
                },
            )

    class SignupAJAXBenchmarkTestCase(SignUpAJAXTestCase, BenchmarkMixin):
        def test_benchmark(self):
            """Perform benchmark and print results."""
            b = self.benchmark([self.test_ajax_validation_errors], 100)
            b.report(
                "ajax-signup", baselines={"test_ajax_validation_error": 1.0}
            )


except ImportError:
    pass

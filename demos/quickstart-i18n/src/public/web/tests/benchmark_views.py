""" ``benchmark_views`` module.
"""

from public.web.tests.test_views import ErrorTestCase, PublicTestCase

from wheezy.http.functional import BenchmarkMixin


class PublicBenchmarkTestCase(PublicTestCase, ErrorTestCase, BenchmarkMixin):
    def runTest(self):  # noqa: N802
        """Perform bachmark and print results."""
        b = self.benchmark(
            (
                self.test_root,
                self.test_home,
                self.test_error_400,
                self.test_error_403,
                self.test_error_404,
            ),
            1000,
        )
        b.report(
            "public",
            baselines={
                "test_root": 1.0,
                "test_home": 1.0,
                "test_error_400": 1.0,
                "test_error_403": 1.0,
                "test_error_404": 1.0,
            },
        )


class StaticFilesBenchmarkTestCase(
    PublicTestCase, ErrorTestCase, BenchmarkMixin
):
    def runTest(self):  # noqa: N802
        """Perform bachmark and print results."""
        b = self.benchmark(
            (
                self.test_static_files,
                self.test_static_file_not_found,
                self.test_static_file_forbidden,
            ),
            1000,
        )
        b.report(
            "static",
            baselines={
                "test_static_files": 1.00,
                "test_static_file_not_found": 1.0,
                "test_static_file_forbidden": 1.0,
            },
        )

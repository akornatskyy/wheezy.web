
""" ``benchmark_hello`` module.
"""

from wheezy.core.benchmark import Benchmark

from test_hello import HelloTestCase


class BenchmarkTestCase(HelloTestCase):
    """
        ../../env/bin/nosetests-2.7 -qs -m benchmark benchmark_hello.py
    """

    def runTest(self):
        """ Perform bachmark and print results.
        """
        p = Benchmark((
            self.test_welcome,
            self.test_home
        ), 20000)
        p.report('hello', baselines={
            'test_welcome': 1.0,
            'test_home': 0.9
        })

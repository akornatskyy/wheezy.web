
""" ``comp`` module.
"""

import sys


PY3 = sys.version_info[0] >= 3

if PY3:  # pragma: nocover
    iteritems = lambda d: d.items()
else:  # pragma: nocover
    iteritems = lambda d: d.iteritems()

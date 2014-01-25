"""
"""

from wheezy.validation.rules import int_adapter
from wheezy.validation.rules import length
from wheezy.validation.rules import range
from wheezy.validation.rules import required


identity = lambda min=1, max=None: int_adapter(range(min, max))

password_rules = [required, length(min=8), length(max=12)]

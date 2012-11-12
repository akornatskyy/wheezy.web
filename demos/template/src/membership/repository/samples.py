
"""
"""

from wheezy.core.comp import u


_ = lambda s: s
db = {
    'user': {
        'demo': u('P@ssw0rd'),
        'biz': u('P@ssw0rd')
    },
    'user_role': {
        'demo': ['user'],
        'biz': ['business']
    },
    'password_question': {
        '1': _('Favorite number'),
        '2': _('City of birth'),
        '3': _('Favorite color')
    },
    'account_type': {
        'user': _('User'),
        'business': _('Business')
    }
}

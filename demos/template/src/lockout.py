
from datetime import timedelta

from wheezy.caching.lockout import Counter
from wheezy.caching.lockout import Locker
from wheezy.http.response import forbidden

from config import cache


# region: alerts

def ignore_alert(s, name, counter):
    pass


# region: lockouts and defaults

def lockout_by_id(count=10,
                  period=timedelta(minutes=15),
                  duration=timedelta(hours=1),
                  reset=False,
                  alert=ignore_alert):
    key_func = lambda h: 'id:%s' % h.principal.id
    return Counter(key_func=key_func, count=count,
                   period=period, duration=duration,
                   reset=reset, alert=alert)


def lockout_by_ip(count=10,
                  period=timedelta(minutes=10),
                  duration=timedelta(hours=2),
                  reset=True,
                  alert=ignore_alert):
    key_func = lambda h: 'ip:%s' % h.request.environ['REMOTE_ADDR']
    return Counter(key_func=key_func, count=count,
                   period=period, duration=duration,
                   reset=reset, alert=alert)


def lockout_by_id_ip(count=10,
                     period=timedelta(minutes=20),
                     duration=timedelta(hours=1),
                     reset=True,
                     alert=ignore_alert):
    key_func = lambda h: 'idip:%s:%s' % (
        h.principal.id, h.request.environ['REMOTE_ADDR'])
    return Counter(key_func=key_func, count=count,
                   period=period, duration=duration,
                   reset=reset, alert=alert)


# region: config

locker = Locker(cache, key_prefix='mysite',
                forbid_action=lambda s: forbidden(),
                by_id=lockout_by_id,
                by_ip=lockout_by_ip,
                by_id_ip=lockout_by_id_ip)

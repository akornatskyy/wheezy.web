"""
"""

from datetime import datetime
from datetime import timedelta

from wheezy.caching.lockout import Counter
from wheezy.caching.lockout import Locker
from wheezy.http.response import forbidden

from config import cache
from config import config

from wheezy.core.mail import MailMessage
from wheezy.core.mail import SMTPClient


# region: alerts

mode = config.get('runtime', 'lockout')


def ignore_alert(s, name, counter, extra=None):
    pass

if mode == 'ignore':
    mail_alert = ignore_alert
elif mode == 'mail':
    def mail_alert(handler, name, counter, extra=None):
        expires_at = (
            datetime.utcnow() + timedelta(seconds=counter.duration)
        ).strftime('%Y/%m/%d %H:%M:%S UTC')
        send_mail(content=handler.render_template(
            'mail/lockout.html',
            name=name,
            c=counter,
            remote_addr=handler.request.environ['REMOTE_ADDR'],
            expires_at=expires_at,
            extra=extra))
else:
    raise NotImplementedError(mode)


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


# region: delivery

def send_mail(content):
    smtp_client.send(MailMessage(
        subject,
        content,
        from_addr,
        to_addrs,
        content_type='text/html',
        charset='UTF-8'))


# region: config

locker = Locker(cache, key_prefix='mysite',
                forbid_action=lambda s: forbidden(),
                by_id=lockout_by_id,
                by_ip=lockout_by_ip,
                by_id_ip=lockout_by_id_ip)

smtp_client = SMTPClient(config.get('mail', 'host'))
from_addr = config.get('lockout_report', 'from-addr')
to_addrs = config.get('lockout_report', 'to-addrs').split(';')
subject = config.get('lockout_report', 'subject')

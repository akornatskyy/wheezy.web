
"""
"""

import os
import platform
import resource
import socket
import sys

from datetime import timedelta
from time import time


start_time = time()


def error_report_extra_provider(request):
    ts = os.times()
    e = request.environ
    r = resource.getrusage(resource.RUSAGE_SELF)
    if 'CONTENT_LENGTH' in e:
        form = filter_names(request.form, ignore=(
            'password',
            'confirm_password'
        ))
    else:
        form = {}
    return {
        'HTTP_ACCEPT_LANGUAGE': e['HTTP_ACCEPT_LANGUAGE'],
        'HTTP_REFERER': e.get('HTTP_REFERER', '?'),
        'HTTP_USER_AGENT': e['HTTP_USER_AGENT'],
        'PATH_INFO': e['PATH_INFO'],
        'REMOTE_ADDR': e['REMOTE_ADDR'],
        'REQUEST_METHOD': e['REQUEST_METHOD'],
        'executable': sys.executable,
        'hostname': socket.gethostname(),
        'http_cookies': request.cookies,
        'http_form': form,
        'machine': platform.machine(),
        'modules': modules_info(),
        'process_uptime': timedelta(seconds=time() - start_time),
        'python_compiler': platform.python_compiler(),
        'python_version': platform.python_version(),
        'release': platform.release(),
        'route_args': dict(e['route_args']),
        'ru_idrss': r[4],
        'ru_inblock': r[9],
        'ru_isrss': r[5],
        'ru_ixrss': r[3],
        'ru_majflt': r[7],
        'ru_maxrss': r[2],
        'ru_minflt': r[6],
        'ru_msgrcv': r[12],
        'ru_msgsnd': r[11],
        'ru_nivcsw': r[15],
        'ru_nsignals': r[13],
        'ru_nswap': r[8],
        'ru_nvcsw': r[14],
        'ru_oublock': r[10],
        'ru_stime': r[1],
        'ru_utime': r[0],
        'stime': timedelta(seconds=ts[1]),
        'system': platform.system(),
        'utime': timedelta(seconds=ts[0]),
        'uwsgi.version': e.get('uwsgi.version', '?'),
    }


def filter_names(d, ignore):
    return dict((name, d[name]) for name in d if name not in ignore)


def modules_info():
    def predicate(m):
        return (hasattr(m, '__version__')
                and not (m.__name__.startswith('_') or '._' in m.__name__))
    return sorted([(m.__name__, m.__version__) for m in sys.modules.values()
                   if predicate(m)])


ERROR_REPORT_FORMAT = """
%(message)s

Environ Variables
-----------------
PATH_INFO: %(PATH_INFO)s
REQUEST_METHOD: %(REQUEST_METHOD)s
REMOTE_ADDR: %(REMOTE_ADDR)s
HTTP_REFERER: %(HTTP_REFERER)s
HTTP_ACCEPT_LANGUAGE: %(HTTP_ACCEPT_LANGUAGE)s
HTTP_USER_AGENT: %(HTTP_USER_AGENT)s

HTTP Request
------------
Route: %(route_args)s
Cookies: %(http_cookies)s
Form: %(http_form)s

Hosting Process
---------------
Process Id: %(process)d
Up Time: %(process_uptime)s
User Time: %(utime)s
System Time: %(stime)s
Maximum Resident Set Size: %(ru_maxrss)s
Shared Memory Size: %(ru_ixrss)s
Page Faults Not Requiring I/O: %(ru_minflt)s
Page Faults Requiring I/O: %(ru_majflt)s
Number of Swap Outs: %(ru_nswap)s
Block Input Operations: %(ru_inblock)s
Block Output Operations: %(ru_oublock)s
Voluntary Context Switches: %(ru_nvcsw)s
Involuntary Context Switches: %(ru_nivcsw)s

Machine Platform
----------------
Host: %(hostname)s
OS: %(system)s %(release)s %(machine)s
Python Version: %(python_version)s [%(python_compiler)s]
uWSGI Version: %(uwsgi.version)s
Executable: %(executable)s
Timestamp: %(asctime)s

Loaded Modules
--------------
%(modules)s


"""

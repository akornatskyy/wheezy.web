"""
"""

from datetime import timedelta

from wheezy.http import CacheProfile
from wheezy.http.cache import etag_md5crc32

from config import config


membership_cache_profile = CacheProfile(
    'both',
    duration=timedelta(minutes=10),
    # this cause browser to send request each time
    # so the server is able to respond with code 304
    http_max_age=0,
    vary_environ=['HTTP_ACCEPT_ENCODING'],
    vary_cookies=['_a'],
    http_vary=['Cookie'],
    etag_func=etag_md5crc32,
    enabled=config.getboolean('cache-profile', 'membership-enabled'))

"""
"""

from datetime import timedelta

from wheezy.http import CacheProfile
from wheezy.http.cache import etag_md5crc32

from config import config


static_cache_profile = CacheProfile(
    'public',
    duration=timedelta(minutes=15),
    vary_environ=['HTTP_ACCEPT_ENCODING'],
    namespace='static',
    enabled=config.getboolean('cache-profile', 'static-enabled'))
public_cache_profile = CacheProfile(
    'both',
    duration=timedelta(minutes=15),
    vary_environ=['HTTP_ACCEPT_ENCODING'],
    vary_cookies=['_a'],
    http_vary=['Cookie'],
    etag_func=etag_md5crc32,
    enabled=config.getboolean('cache-profile', 'public-enabled'))

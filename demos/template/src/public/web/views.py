"""
"""

from wheezy.web.handlers import template_handler

extra = {
    'translation_name': 'public'
}

home = template_handler('public/home.html', **extra)
about = template_handler('public/about.html', **extra)

http400 = template_handler('public/http400.html', status_code=400, **extra)
http403 = template_handler('public/http403.html', status_code=403, **extra)
http404 = template_handler('public/http404.html', status_code=404, **extra)
http500 = template_handler('public/http500.html', status_code=500, **extra)

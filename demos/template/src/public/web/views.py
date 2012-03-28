"""
"""

from wheezy.web.handlers import template_handler


home = template_handler('public/home.html')
about = template_handler('public/about.html')

http400 = template_handler('public/http400.html', status_code=400)
http403 = template_handler('public/http403.html', status_code=403)
http404 = template_handler('public/http404.html', status_code=404)
http500 = template_handler('public/http500.html', status_code=500)

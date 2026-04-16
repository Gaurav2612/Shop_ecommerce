"""
WSGI config for gk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""
import sys
import os

project_home = '/home/Golu827009/shoes_shop'
if project_home not in sys.path:
    sys.path.insert(0, project_home)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gk.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import os
import sys
sys.path.append('home/toilet/toilet_mapper/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'toilet_mapper.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

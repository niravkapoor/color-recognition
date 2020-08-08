import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detect_fruit.settings')

application = get_wsgi_application()

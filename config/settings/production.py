from .development import *

DEBUG = False

DATABASES = {
    # production database configuration
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jacobfelknor$sterling',
            'USER': 'jacobfelknor',
            'PASSWORD': db_password,
            'HOST': 'jacobfelknor.mysql.pythonanywhere-services.com',
        }
}

ALLOWED_HOSTS.append('jacobfelknor.pythonanywhere.com')
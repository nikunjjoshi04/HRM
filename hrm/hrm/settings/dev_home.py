from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'niknoke04@gmail.com'
EMAIL_HOST_PASSWORD = ''
<<<<<<< HEAD
EMAIL_PORT = 587
=======
EMAIL_PORT = 587
>>>>>>> 48b8e6c08a47d878f810baf92d11fb6a6ca97c2e

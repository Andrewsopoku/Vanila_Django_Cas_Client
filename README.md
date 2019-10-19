# Vanila_Django_Cas_Client
Easy way to connect your Django application to a CAS server


NOTE: I use this app to illustrate how CAS Clients works. I shall clean, write some tests.

# Functionality
Supports Token auth schemes
Support Single Sign Out
Can fetch Proxy Granting Ticket
Supports Django 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11 and 2.x
Supports Python 3.x



# Settings
Now add it to the middleware, authentication backends and installed apps in your settings. Make sure you also have the authentication middleware installed. Here's an example:

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'vanila_djangocore_cas',
        ...
    )


    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'vanila_djangocore_cas.backends.CASBackend',
    )

# Set the following required setting in settings.py:

Set it to the base URL of your CAS source (e.g. https://account.company.com/cas/).

    CAS_SERVER_URL = ""

    CAS_VERSION="3"
    CAS_REDIRECT_ON_LOGOUT="/"
    CAS_REDIRECT_ON_LOGIN="/"
    CAS_NEXT_DEFAULT="/admin/"
    CAS_REDIRECT_URL="/"
    CAS_STORE_NEXT = True
    CAS_USERNAME_ATTRIBUTE = 'uid'

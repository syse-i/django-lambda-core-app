# Lambda - Core

...

## Installation


Add the following apps to ``INSTALLED_APPS``:

```
INSTALLED_APPS = [
    ...
    'django_su',  # must be before ``django.contrib.admin``,
    'django.contrib.sites',
    'registration',
    'django.contrib.admin',
    ...
    'django_extensions',
    'ajax_select',
    'maintenance_mode',
    'lambda_theme',
    'lambda_core',
    ...
]
```

Add the following backends to ``AUTHENTICATION_BACKENDS`` :

```
AUTHENTICATION_BACKENDS = (
    ...
    'django_su.backends.SuBackend',
)
```

Add the following middlewares to ``MIDDLEWARE``

```
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware', # as last middleware
]
```

Add the following context processors to ``CONTEXT_PROCESSORS``


```
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                ...
                'django_su.context_processors.is_su',
                'maintenance_mode.context_processors.maintenance_mode',
            ],
        },
    },
]
```

Add your custom templates/503.html file

Include the following urls in your project urls:

```
path('core/', include('lambda_core.urls')),
path('su/', include('django_su.urls')),
```

Add this configuration defaults:

```

# Django Sites Framework
# https://docs.djangoproject.com/en/2.2/ref/contrib/sites/#enabling-the-sites-framework

SITE_ID = 1


# Django Lambda Theme
# https://gitlab.com/lambda-software/django-lambda-theme

LAMBDA_THEME = 'tailwindcss'

LAMBDA_THEME_LOGIN_URL = 'auth_login'
LAMBDA_THEME_LOGOUT_URL = 'auth_logout'


# Django Su
# https://github.com/adamcharnock/django-su

AJAX_LOOKUP_CHANNELS = {'django_su':  dict(model='auth.user', search_field='username')}

# URL to redirect after the login.
# Default: "/"
SU_LOGIN_REDIRECT_URL = "/"

# URL to redirect after the logout.
# Default: "/"
SU_LOGOUT_REDIRECT_URL = "/"


# Maintenance Mode
# https://github.com/fabiocaccamo/django-maintenance-mode

MAINTENANCE_MODE = False

# if True admin site will not be affected by the maintenance-mode page
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True

# if True authenticated users will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_AUTHENTICATED_USER = True

```

3. Run `python manage.py migrate` to create the core models.


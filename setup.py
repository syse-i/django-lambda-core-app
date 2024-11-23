import os
from setuptools import setup

from lambda_core import __version__


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-lambda-core',
    version=__version__,
    packages=['lambda_core'],
    install_requires=[
        # Our dependencies
        'django-lambda-config',
        'django-lambda-theme',
        'django-lambda-theme-tailwindcss',
        'django-lambda-url',
        #'django-lambda-config',
        #'django-lambda-theme',
        #'django-lambda-theme-tailwindcss',
        #'django-lambda-url',
        # Third party dependencies
        'boto3',
        'django-allauth',
        'django-compat',
        'django-extensions',
        'django-guardian',
        'django-hijack',
        'django-maintenance-mode',
        'django-notifications-hq',
        'django-reversion',
        'django-sendgrid-v5',
        'django-storages',
        'django',
        'djangorestframework',
        'fabric',
        'gunicorn',
        'ipython',
        'markdown',
        'pillow',
        'psycopg2-binary',
        'pyyaml',
        'sendgrid',
        'sentry-sdk',
        'django-cors-headers',
        'django-rest-knox',
        'django-filter',
        'django-debug-toolbar',
    ],
    dependency_links=[
        'git+https://github.com/syse-i/django-lambda-config.git@main#egg=django-lambda-config',
        'git+https://github.com/syse-i/django-lambda-theme.git@main#egg=django-lambda-theme',
        'git+https://bitbucket.org/lambda_software/django-lambda-theme-tailwindcss.git#egg=django-lambda-theme-tailwindcss',
        'git+https://github.com/syse-i/django-lambda-url.git#egg=django-lambda-url'
    ],
    include_package_data=True,
    license='BSD License',  # example license
    description='SYSE-I Django Core App',
    long_description=README,
    url='https://www.syse-i.net/',
    author='David Sosa Valdes',
    author_email='david.sosa.valdes@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

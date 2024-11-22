import os
import errno

from django.conf import settings
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from django.template.loader import render_to_string
from django.core.management.base import CommandError

from lambda_core.management.commands import LambdaCommand
from lambda_core.management.config import SERVER_BASE_DIR


class Command(LambdaCommand):
    help = 'Lambda | Config Command'

    def handle(self, *args, **kwargs):
        super().handle(*args, **kwargs)

        if not os.path.exists(settings.LAMBDA_EXTENSIONS_DIR):
            try:
                os.makedirs(settings.LAMBDA_EXTENSIONS_DIR)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        user, group = ('ubuntu', 'www-data')

        try:
            app = self.config['application']
            server = self.config['server']

            app_name = app['name']
            app_dir = os.path.join(SERVER_BASE_DIR, app_name)
            app_conf_dir = os.path.join(app_dir, 'conf')
            app_venv_dir = os.path.join(app_dir, '.venv')
            app_htdocs_dir = os.path.join(app_dir, 'public_html')
            app_logs_dir = os.path.join(app_dir, 'logs')
            upstream_name = app_name.replace('.', '_')
            web_socket = os.path.join(app_htdocs_dir, 'web.sock')
            branch = app.get('branch', 'master')

            try:
                app_environment = app['environment']
            except KeyError:
                app_environment = {}

            try:
                server_packages = server['packages']
            except KeyError:
                server_packages = []

            try:
                django_commands = app['django']['run']
            except KeyError:
                django_commands = []

            files = {
                os.path.join(settings.LAMBDA_EXTENSIONS_DIR, 'nginx.conf'): render_to_string(
                    'lambda_core/management/commands/config/nginx.conf.template', context={
                        'user': 'user',
                        'group': group,
                    }
                ),
                os.path.join(settings.LAMBDA_EXTENSIONS_DIR, 'nginx.vhost.conf'): render_to_string(
                    'lambda_core/management/commands/config/nginx.vhost.conf.template', context={
                        'upstream_name': upstream_name,
                        'web_socket': web_socket,
                        'server_name': app_name,
                        'root': app_htdocs_dir,
                        'access_log': os.path.join(app_logs_dir, 'access.log'),
                        'error_log': os.path.join(app_logs_dir, 'error.log'),
                    }
                ),
                os.path.join(settings.LAMBDA_EXTENSIONS_DIR, 'nginx.vhost-setup.conf'): render_to_string(
                    'lambda_core/management/commands/config/nginx.vhost-setup.conf.template', context={
                        'upstream_name': upstream_name,
                        'web_socket': web_socket,
                        'server_name': app_name,
                        'root': app_htdocs_dir,
                        'access_log': os.path.join(app_logs_dir, 'access.log'),
                        'error_log': os.path.join(app_logs_dir, 'error.log'),
                    }
                ),
                os.path.join(settings.LAMBDA_EXTENSIONS_DIR, 'gunicorn.service'): render_to_string(
                    'lambda_core/management/commands/config/gunicorn.service.template', context={
                        'server_name': app_name,
                        'user': user,
                        'group': group,
                        'working_directory': app_htdocs_dir,
                        'environment_file': os.path.join(app_dir, '.env.gunicorn'),
                        'venv_directory': app_venv_dir,
                        'web_socket': web_socket
                    }
                ),
            }

            fabric_config = {
                'BASE_DIR': os.environ.get('SERVER_HOME_DIR', '/home/ubuntu'),
                'APP_NAME': app_name,
                'APP_DIR': app_dir,
                'APP_CONF_DIR': app_conf_dir,
                'APP_VENV_DIR': app_venv_dir,
                'APP_HTDOCS_DIR': app_htdocs_dir,
                'APP_LOGS_DIR': app_logs_dir,
                'REPOSITORY_URL': app['repository'],
                'BRANCH': branch,
                'PACKAGES': server_packages,
                'DJANGO_COMMANDS': django_commands,
                'SSL_SETUP': app.get('ssl_setup', False),
                'LAMBDA_EXTENSIONS_DIR': os.path.join(settings.BASE_DIR, '.lambda_extensions'),
                'GUNICORN_SERVICE': '/etc/systemd/system/%s.service' % app_name,
                'NGINX_VHOST_FILE': '/etc/nginx/sites-enabled/%s.conf' % app_name,
            }

            stream = open(os.path.join(settings.LAMBDA_EXTENSIONS_DIR, 'fabric.yaml'), 'w')
            dump(fabric_config, stream, Dumper=Dumper)

            for (filename, out) in files.items():
                with open(filename, "w+b") as f:
                    f.truncate()
                    f.write(out.encode('utf-8'))

            if not app_environment:
                self.stdout.write(self.style.NOTICE('There is no ENV VARS in the configuration file...'))
            else:
                with open(os.path.join(settings.LAMBDA_EXTENSIONS_DIR, 'env'), "w+b") as f:
                    f.truncate()
                    out = ''
                    for (key, value) in app_environment.items():
                        out += 'export {}="{}"\n'.format(key, value)
                    f.write(out.encode('utf-8'))
        except KeyError:
            raise CommandError(Exception('There is a problem with the config file...'))

        self.stdout.write('Generating config files: [%s]' % self.style.SUCCESS('SUCCESS'))

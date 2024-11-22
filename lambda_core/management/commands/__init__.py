import os
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from fabric import Connection

from django.conf import settings
from django.core.management import BaseCommand


# noinspection PyAbstractClass
class LambdaCommand(BaseCommand):
    _config = None

    def add_arguments(self, parser):
        parser.add_argument(
            'config_file', type=str, nargs='?',
            default=os.path.join(settings.LAMBDA_CONFIG_DIR, 'config.yaml')
        )

    @staticmethod
    def load_yaml(file_path):
        stream = open(file_path, 'r').read()
        return load(stream, Loader=Loader)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, file_path):
        self._config = self.load_yaml(file_path)

    def handle(self, *args, **kwargs):
        self.config = kwargs['config_file']


# noinspection PyAbstractClass
class LambdaFabricCommand(LambdaCommand):

    def run_function(self, connection, config):
        pass

    def handle(self, *args, **kwargs):
        super().handle(*args, **kwargs)
        connection = Connection(**self.config['server']['connection'])
        fabric_config = self.load_yaml(os.path.join(settings.LAMBDA_EXTENSIONS_DIR, 'fabric.yaml'))
        self.run_function(connection, fabric_config)
        self.stdout.write('Deployment status: [%s]' % self.style.SUCCESS('SUCCESS'))

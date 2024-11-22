from lambda_core.management.commands import LambdaFabricCommand
from lambda_core.fabric import setup


class Command(LambdaFabricCommand):
    help = 'Lambda | Deploy Command'

    def run_function(self, connection, config):
        return setup(connection, config)

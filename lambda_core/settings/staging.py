from lambda_config.settings import staging
from lambda_core.settings import base


class Settings(base.Settings, staging.Settings):
    pass

from lambda_core.settings import base


class BaseSettings(base.Settings):
    BASE_DIR = base.BaseDir(__file__)

from lambda_core.settings import staging

from .base import BaseSettings


class Settings(BaseSettings, staging.Settings):
    pass


Settings.load()

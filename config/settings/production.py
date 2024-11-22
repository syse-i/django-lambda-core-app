from lambda_core.settings import production

from .base import BaseSettings


class Settings(BaseSettings, production.Settings):
    pass


Settings.load()

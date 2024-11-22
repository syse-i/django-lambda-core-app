from lambda_core.settings import local

from .base import BaseSettings


class Settings(BaseSettings, local.Settings):
    pass


Settings.load()

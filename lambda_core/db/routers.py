from django.conf import settings


class BlockMigrationsRouter:

    # noinspection PyMethodMayBeStatic
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        try:
            if db == 'default':
                return True
            return settings.DATABASES[db]['allow_migrate']
        except KeyError:
            pass
        return None

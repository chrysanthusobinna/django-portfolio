from django.apps import AppConfig
from importlib import import_module

class PortfolioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio_app'

    def ready(self):
        import_module(f'{self.name}.signals')

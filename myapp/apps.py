from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

class MyappConfig(AppConfig):
    name = 'myapp'
    
    def ready(self):
        # Import signals after app is ready
        from . import signals
from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
    
    def ready(self):
        """
        Import signals when the app is ready.
        This ensures that signal handlers are registered when Django starts.
        """
        import messaging.signals

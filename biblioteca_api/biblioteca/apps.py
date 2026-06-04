from django.apps import AppConfig


class BibliotecaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biblioteca'
    verbose_name = 'Sistema de Gestión de Biblioteca'

    def ready(self):
        pass

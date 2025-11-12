# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\apps.py

from django.apps import AppConfig

class MiAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mi_admin'

    def ready(self):
        # --- ESTA ES LA CORRECCIÓN ---
        # DESCOMENTA esta línea para que tus señales se registren y funcionen.
        import mi_admin.signals
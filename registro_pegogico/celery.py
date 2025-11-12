import os
from celery import Celery

# Configura el 'DJANGO_SETTINGS_MODULE' para el programa 'celery'.
# Reemplaza 'registro_pegogico' si el nombre de tu proyecto es otro.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registro_pegogico.settings')

app = Celery('registro_pegogico')

# Usa un string aquí para que el worker no tenga que serializar
# el objeto de configuración.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga automáticamente los módulos de tareas de todas las apps registradas
# (buscará un archivo tasks.py en cada app, como en 'mi_admin/tasks.py')
app.autodiscover_tasks()
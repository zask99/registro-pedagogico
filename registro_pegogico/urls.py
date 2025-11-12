# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\registro_pegogico\urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='mi_admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # CAMBIO AQUÍ: Incluye las URLs de la aplicación 'mi_admin' directamente en la raíz
    path('', include('mi_admin.urls', namespace='mi_admin')), # <--- Important!

    # Asegúrate de que la línea anterior 'path('docente/', include('mi_admin.urls'))'
    # esté COMENTADA o ELIMINADA si no quieres ese prefijo.
]
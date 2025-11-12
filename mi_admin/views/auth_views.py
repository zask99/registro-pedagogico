# mi_admin/views/auth_views.py

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# --- IMPORTANTE: Importa tus modelos de perfil ---
from mi_admin.models import Docente, Estudiante, Administrativo

# --- Logout personalizado ---
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect(reverse_lazy('login'))  # Redirige a login

# --- Redirección basada en rol ---
@login_required
def role_based_redirect(request):
    """
    Redirige al usuario al dashboard correcto según su perfil (Docente, Estudiante, etc.)
    Este método es más robusto que comprobar el string del nombre del rol.
    """
    user = request.user

    # Primero, verifica si el usuario es un superusuario (admin de Django)
    if user.is_superuser:
        # Asumimos que el superusuario es también un Administrativo
        return redirect(reverse_lazy('dashboard_administrativo'))

    # --- INICIO DE LA NUEVA LÓGICA ---
    # Comprobar la existencia del perfil directamente en la base de datos.
    # Esto evita problemas de caché o strings con espacios.

    try:
        # Comprobar si existe un perfil de Docente
        if Docente.objects.filter(persona__usuario=user).exists():
            return redirect(reverse_lazy('dashboard_docente'))
        
        # Comprobar si existe un perfil de Administrativo
        elif Administrativo.objects.filter(persona__usuario=user).exists():
            return redirect(reverse_lazy('dashboard_administrativo'))
        
        # Comprobar si existe un perfil de Estudiante
        elif Estudiante.objects.filter(persona__usuario=user).exists():
            return redirect(reverse_lazy('dashboard_estudiante'))
        
        # Si no tiene ningún perfil...
        else:
            rol_nombre = "Sin Rol"
            if hasattr(user, 'rol') and user.rol:
                rol_nombre = user.rol.nombre
            
            # Este mensaje es ahora más preciso
            messages.warning(request, f"Tu cuenta (Rol: {rol_nombre}) no tiene un perfil (Docente, Estudiante, etc.) creado. Contacta al administrador.")
            return redirect(reverse_lazy('dashboard_generico'))
            
    except Exception as e:
        # Captura cualquier otro error inesperado
        messages.error(request, f"Ocurrió un error inesperado al redirigir: {e}")
        return redirect(reverse_lazy('dashboard_generico'))
    # --- FIN DE LA NUEVA LÓGICA ---
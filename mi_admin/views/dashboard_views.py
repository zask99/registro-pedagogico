# mi_admin/views/dashboard_views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Importa todos los modelos necesarios
from mi_admin.models import (
    Rol, Docente, Asignacion, Estudiante, Administrativo, Persona, Curso
)
import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    user = request.user
    user_rol_name = user.rol.nombre if (hasattr(user, 'rol') and user.rol) else None

    # --- LOGS DETALLADOS ---
    print(f"\n--- INICIO DE REDIRECCIÓN PARA: {user.username} ---")
    logger.info(f"Iniciando redirección para el usuario: {user.username}")
    
    if user.is_superuser:
        print(f"--- DEBUG: El usuario {user.username} es superusuario. Redirigiendo a dashboard_administrativo.")
        logger.info(f"Usuario {user.username} es superusuario. Redirigiendo a admin dashboard.")
        # Superusuarios también necesitan los datos del dashboard admin
        try:
            persona_perfil = Persona.objects.get(usuario=user)
            
            # --- CORRECCIÓN N°1 ---
            # Se busca 'administrativo', no 'administrativo_perfil'
            admin_perfil = persona_perfil.administrativo 
            
            context = {
                'user': user,
                'rol': 'Administrativo (Superuser)',
                'administrativo': admin_perfil,
                'persona': persona_perfil,
                'nombre_admin': persona_perfil.get_full_name()
            }
            return render(request, 'mi_admin/dashboard_administrativo.html', context)
        except Exception as e:
            print(f"--- ERROR: Superusuario {user.username} no tiene perfiles de Persona/Admin. Creándolos...")
            # Si el superusuario no tiene perfiles (ej. creado con createsuperuser)
            # Dales un perfil de admin para que el dashboard funcione
            rol_admin, _ = Rol.objects.get_or_create(nombre='administrativo')
            user.rol = rol_admin
            user.save()
            persona, _ = Persona.objects.get_or_create(usuario=user, defaults={'nombres': user.username, 'apellidos': 'Admin'})
            admin_perfil, _ = Administrativo.objects.get_or_create(persona=persona, defaults={'cargo': 'Superusuario'})
            
            # Reintenta la carga
            context = {
                'user': user,
                'rol': 'Administrativo (Superuser)',
                'administrativo': admin_perfil,
                'persona': persona,
                'nombre_admin': persona.get_full_name()
            }
            return render(request, 'mi_admin/dashboard_administrativo.html', context)


    # Comprobar si el usuario tiene un perfil de Persona
    try:
        persona_perfil = Persona.objects.get(usuario=user)
        print(f"--- DEBUG: Usuario {user.username} tiene un perfil de Persona: {persona_perfil.get_full_name()}")
    except Persona.DoesNotExist:
        error_message = f"No se encontró perfil de Persona para el usuario '{user.username}'. Esto es un problema de configuración de datos."
        print(f"--- ERROR: {error_message}")
        messages.error(request, "Error crítico: Tu cuenta de usuario no está vinculada a un perfil de Persona. Contacta al administrador.")
        return render(request, 'mi_admin/dashboard_generico.html', {'user': user, 'rol': user_rol_name, 'error_message': error_message})
    except Exception as e:
        error_message = f"Error al obtener perfil de Persona: {e}"
        print(f"--- ERROR: {error_message}")
        return render(request, 'mi_admin/dashboard_generico.html', {'user': user, 'rol': user_rol_name, 'error_message': error_message})


    # --- INICIO DE LA LÓGICA CORREGIDA (N°2) ---
    # Usamos hasattr() para comprobar los related_name correctos:
    # 'administrativo', 'docente', 'estudiante'
    try:
        # 1. Comprobar si existe el perfil 'administrativo'
        has_admin_perfil = hasattr(persona_perfil, 'administrativo')
        print(f"--- DEBUG: ¿Tiene 'administrativo'? -> {has_admin_perfil}")
        if has_admin_perfil:
            print(f"--- ÉXITO: Renderizando dashboard_administrativo para {user.username}.")
            context = {
                'user': user,
                'rol': user_rol_name,
                'administrativo': persona_perfil.administrativo, # <-- CORREGIDO
                'persona': persona_perfil,
                'nombre_admin': persona_perfil.get_full_name()
            }
            return render(request, 'mi_admin/dashboard_administrativo.html', context)
        
        # 2. Comprobar si existe el perfil 'docente'
        has_docente_perfil = hasattr(persona_perfil, 'docente')
        print(f"--- DEBUG: ¿Tiene 'docente'? -> {has_docente_perfil}")
        if has_docente_perfil:
            print(f"--- ÉXITO: Renderizando dashboard_docente para {user.username}.")
            docente = persona_perfil.docente # <-- CORREGIDO
            asignaciones = Asignacion.objects.filter(docente=docente).select_related('curso', 'materia').order_by('curso__grado', 'curso__paralelo', 'materia__nombre')
            
            context = {
                'user': user,
                'rol': user_rol_name,
                'docente': docente,
                'asignaciones_docente': asignaciones, # Pasado para el modal
                'persona': persona_perfil,
                'nombre_docente': persona_perfil.get_full_name()
            }
            return render(request, 'mi_admin/dashboard_docente.html', context)
        
        # 3. Comprobar si existe el perfil 'estudiante'
        has_estudiante_perfil = hasattr(persona_perfil, 'estudiante')
        print(f"--- DEBUG: ¿Tiene 'estudiante'? -> {has_estudiante_perfil}")
        if has_estudiante_perfil:
            print(f"--- ÉXITO: Renderizando dashboard_estudiante para {user.username}.")
            context = {
                'user': user,
                'rol': user_rol_name,
                'estudiante': persona_perfil.estudiante, # <-- CORREGIDO
                'persona': persona_perfil,
            }
            return render(request, 'mi_admin/dashboard_estudiante.html', context)
        
        # 4. Si no tiene NINGÚN perfil
        else:
            error_message = f"Rol '{user_rol_name or 'Ninguno'}' no tiene un perfil específico (Docente, Estudiante, etc.) creado."
            print(f"--- FALLO: {error_message}. Redirigiendo a dashboard genérico.")
            messages.warning(request, f"Tu cuenta (Rol: {user_rol_name}) no tiene un perfil (Docente, Estudiante, etc.) creado. Contacta al administrador.")
            return render(request, 'mi_admin/dashboard_generico.html', {'user': user, 'rol': user_rol_name, 'error_message': error_message})
            
    except Exception as e:
        error_message = f"Error inesperado al comprobar perfiles: {e}"
        print(f"--- ERROR CRÍTICO: {error_message}")
        logger.error(f"Excepción en dashboard para {user.username}: {e}", exc_info=True)
        return render(request, 'mi_admin/dashboard_generico.html', {'user': user, 'rol': user_rol_name, 'error_message': error_message})
    # --- FIN DE LA LÓGICA CORREGIDA ---
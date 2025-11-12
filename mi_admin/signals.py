# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Rol, Persona, Docente, Estudiante, Administrativo
import logging

logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Usuario)
# def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
#     """
#     Al crear o actualizar un Usuario, crea/actualiza la Persona y luego el perfil correspondiente.
#     """
    
#     # Si el usuario es superusuario o no tiene rol asignado, no hacemos nada con perfiles.
#     if instance.is_superuser or not instance.rol:
#         return

#     rol_nombre = instance.rol.nombre.lower().strip() # Usar lower() y strip()

#     # Obtener o crear la Persona
#     # Usamos los datos del Usuario para pre-llenar la Persona
#     persona_data = {
#         'nombres': instance.first_name or '',
#         'apellidos': instance.last_name or '',
#         # Los campos eliminados (ci, genero, correo_personal, etc.) ya no se añaden
#     }
    
#     persona, persona_created = Persona.objects.get_or_create(
#         usuario=instance, 
#         defaults=persona_data
#     )

#     # Si la persona ya existía (created=False), actualizamos sus datos básicos
#     if not persona_created:
#         persona.nombres = instance.first_name or persona.nombres
#         persona.apellidos = instance.last_name or persona.apellidos
#         persona.save()

#     # PASO 2: Crear el perfil específico y vincularlo a la Persona
#     try:
#         if rol_nombre == 'docente':
#             Docente.objects.get_or_create(persona=persona)
#             # Eliminar otros perfiles si existen
#             Estudiante.objects.filter(persona=persona).delete()
#             Administrativo.objects.filter(persona=persona).delete()
#             logger.info(f"Perfil de Docente asegurado para {instance.username}")

#         elif rol_nombre == 'estudiante':
#             Estudiante.objects.get_or_create(persona=persona)
#             # Eliminar otros perfiles si existen
#             Docente.objects.filter(persona=persona).delete()
#             Administrativo.objects.filter(persona=persona).delete()
#             logger.info(f"Perfil de Estudiante asegurado para {instance.username}")

#         elif rol_nombre == 'administrativo':
#             Administrativo.objects.get_or_create(persona=persona, defaults={'cargo': 'Por definir'})
#             # Eliminar otros perfiles si existen
#             Docente.objects.filter(persona=persona).delete()
#             Estudiante.objects.filter(persona=persona).delete()
#             logger.info(f"Perfil de Administrativo asegurado para {instance.username}")
            
#     except Exception as e:
#         logger.error(f"Error al crear/actualizar perfil para {instance.username}: {e}")
# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\views\api_views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import Asignacion, Curso, Docente, Persona # Asegúrate de que Asignacion, Curso, Docente y Persona estén bien importados
import logging

logger = logging.getLogger(__name__)

# Función de verificación de rol (ajusta si tu lógica es diferente)
def es_admin(user):
    # Asegúrate de que el usuario tenga un rol y que su nombre sea 'Administrador'
    return user.is_authenticated and hasattr(user, 'rol') and user.rol and user.rol.nombre == 'Administrador'

@login_required
@user_passes_test(es_admin)
def api_get_course_assignments(request, curso_id):
    """
    Vista API que devuelve las asignaciones de materias y docentes para un curso específico.
    """
    try:
        curso = get_object_or_404(Curso, pk=curso_id)

        # Usar select_related para obtener Materia, Docente y Persona en una sola consulta
        asignaciones = Asignacion.objects.filter(curso=curso).select_related(
            'materia',
            'docente',
            'docente__persona' # Esto es crucial para acceder a los datos de Persona del Docente
        ).order_by('materia__nombre')

        data = []
        for asignacion in asignaciones:
            docente_nombre = None
            if asignacion.docente and asignacion.docente.persona:
                docente_nombre = asignacion.docente.persona.get_full_name() # Usar el método get_full_name

            data.append({
                'id': asignacion.id, # Puede ser útil para futuras acciones de editar/eliminar
                'materia_nombre': asignacion.materia.nombre,
                'docente_nombre': docente_nombre,
                'anio_academico': asignacion.anio_academico,
                # Puedes añadir más campos si los necesitas en el modal
            })
        
        logger.info(f"Asignaciones cargadas para curso {curso_id}: {len(data)} elementos.")
        return JsonResponse({'asignaciones': data})

    except Curso.DoesNotExist:
        logger.warning(f"Intento de acceder a asignaciones de curso inexistente: {curso_id}")
        return JsonResponse({'error': 'Curso no encontrado.'}, status=404)
    except Exception as e:
        logger.exception(f"Error inesperado al obtener asignaciones para curso {curso_id}")
        return JsonResponse({'error': 'Error interno del servidor al cargar las asignaciones.', 'details': str(e)}, status=500)
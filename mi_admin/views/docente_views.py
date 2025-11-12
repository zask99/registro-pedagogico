# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\views\docente_views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from decimal import Decimal
from datetime import  date, timedelta
from django.http import Http404
from django.urls import reverse # Importar reverse para construir URLs
from urllib.parse import urlencode # Importar urlencode para construir parámetros GET
from django.db import transaction # Importar transaction para atomic operations
from collections import defaultdict # Importar defaultdict para los diccionarios de asistencia
import logging
logger = logging.getLogger(__name__)
from django.db.models import Q
from mi_admin.models import Inscripcion

from mi_admin.models import (
    Curso, Estudiante, Docente, Asistencia, Asignacion, Trimestre,
    TipoComponente, Subcomponente, Evaluacion, Nota,
)
from mi_admin.permissions import is_docente # Asumo que esta importación es correcta


@login_required
@user_passes_test(is_docente, login_url='/')
def dashboard_docente(request):
    """
    Vista principal (Dashboard) para el docente.
    Muestra la bienvenida y carga los datos para el modal de perfil.
    """
    logger.debug(f"[{request.user.username}] Accediendo a dashboard_docente_view")
    try:
        # 1. Obtener el objeto Docente y su Persona (para datos personales)
        # Usamos select_related para optimizar la consulta a la tabla Persona
        docente = get_object_or_404(Docente.objects.select_related('persona'), persona__usuario=request.user)
        
        # 2. Obtener el nombre completo para el saludo
        nombre_completo_docente = docente.persona.get_full_name()

        # 3. Obtener las asignaciones (cursos y materias) para el modal
        asignaciones_docente = Asignacion.objects.filter(
            docente=docente
        ).select_related('materia', 'curso').order_by('curso__grado', 'curso__paralelo', 'materia__nombre')

        # 4. Preparar el contexto para la plantilla
        context = {
            'nombre_docente': nombre_completo_docente,
            'docente': docente, # Pasamos el objeto completo para el modal
            'asignaciones_docente': asignaciones_docente, # Pasamos las asignaciones para el modal
        }
        
        # 5. Renderizar la plantilla
        return render(request, 'mi_admin/dashboard_docente.html', context)
    
    except Docente.DoesNotExist:
        logger.error(f"[{request.user.username}] (Dashboard) No se encontró el perfil de docente asociado.")
        messages.error(request, "Acceso denegado. No tiene un perfil de docente asociado.")
        return redirect('logout') # O a la página de login
    except Exception as e:
        logger.exception(f"[{request.user.username}] (Dashboard) Ocurrió un error inesperado: {e}")
        messages.error(request, f"Ocurrió un error inesperado al cargar el dashboard: {e}")
        # Renderiza la plantilla incluso si hay un error, pero sin datos
        return render(request, 'mi_admin/dashboard_docente.html', {})

# ... (El resto de tus vistas: listar_cursos_docente, listar_estudiantes_por_curso_docente, etc.) ...
# Función auxiliar para obtener el contexto de los cursos asignados (evita duplicación de código)
def _get_docente_cursos_context(docente_obj, current_year, username):
    cursos_asignados_query = Asignacion.objects.filter(
        docente=docente_obj,
    ).select_related('curso', 'materia', 'docente')

    logger.debug(f"[{username}] Consulta de Asignaciones SQL: {cursos_asignados_query.query}")
    logger.debug(f"[{username}] Número de asignaciones encontradas: {cursos_asignados_query.count()}")

    cursos_agrupados = defaultdict(lambda: {
        'id': None,
        'grado': '', # Usar 'grado' y 'paralelo' para coincidir con la plantilla
        'paralelo': '',
        'niveles': '', # Nombre del curso (Grado 'Paralelo' - Nivel)
        'anio_academico': '', # Año académico de la asignación
        'materias': [] # Lista de materias asignadas para este curso
    })
    
    if not cursos_asignados_query.exists():
        # Si no hay asignaciones, retorna una lista vacía y un mensaje
        return [], "No tienes asignaciones de materias para este año académico."

    for asignacion in cursos_asignados_query:
        curso_id = asignacion.curso.id
        if cursos_agrupados[curso_id]['id'] is None:
            cursos_agrupados[curso_id]['id'] = asignacion.curso.id
            cursos_agrupados[curso_id]['grado'] = asignacion.curso.grado # Usar 'grado'
            cursos_agrupados[curso_id]['paralelo'] = asignacion.curso.paralelo # Usar 'paralelo'
            cursos_agrupados[curso_id]['niveles'] = asignacion.curso.get_niveles_display() # Usar 'niveles'
            cursos_agrupados[curso_id]['anio_academico'] = asignacion.anio_academico # Captura el año académico de la asignación

        # Añade los detalles de la materia a la lista de materias del curso
        cursos_agrupados[curso_id]['materias'].append({
            'id': asignacion.materia.id, # ID de la materia
            'nombre': asignacion.materia.nombre, # Nombre de la materia
            'asignacion_id': asignacion.id, # ID de la asignación (para enlaces como "Calificar")
        })
    
    cursos_para_template = list(cursos_agrupados.values())
    logger.debug(f"[{username}] Cursos agrupados para template: {len(cursos_para_template)} cursos.")
    return cursos_para_template, None # Retorna la lista de cursos y None para el mensaje de error


# 
# ***** SE HA ELIMINADO LA FUNCIÓN DUPLICADA DE "dashboard_docente" QUE ESTABA AQUÍ *****
# 


@login_required
@user_passes_test(is_docente, login_url='/')
def listar_cursos_docente(request):
    logger.info(f"[{request.user.username}] Ingresando a listar_cursos_docente")
    try:
        docente = get_object_or_404(Docente, persona__usuario=request.user)
        logger.debug(f"[{request.user.username}] (Listar Cursos) Docente recuperado: {docente.persona.nombres} {docente.persona.apellidos} (ID: {docente.id})")
        
        current_year = timezone.now().year
        
        # Obtener el primer trimestre para el enlace de Calificar por defecto
        # CORRECCIÓN: Cambiado 'orden' a 'numero'
        primer_trimestre = Trimestre.objects.order_by('numero').first()
        primer_trimestre_id = primer_trimestre.id if primer_trimestre else None

        # Usa la función auxiliar para obtener los datos de los cursos
        cursos_para_template, message = _get_docente_cursos_context(docente, current_year, request.user.username)
        
        if message: # Si la función auxiliar retornó un mensaje (es decir, no hay asignaciones)
            messages.info(request, message)
        
        return render(request, 'mi_admin/listar_cursos_docente.html', {
            'cursos_asignados': cursos_para_template,
            'current_year': current_year,
            'primer_trimestre_id': primer_trimestre_id, # Pasa el ID del primer trimestre
        })

    except Docente.DoesNotExist:
        logger.error(f"[{request.user.username}] No se encontró el perfil de docente asociado.")
        messages.error(request, "Acceso denegado. No tiene un perfil de docente asociado.")
        return redirect('mi_admin:dashboard_docente') 
    except Exception as e:
        logger.exception(f"[{request.user.username}] ERROR INESPERADO en listar_cursos_docente: {e}")
        messages.error(request, f"Ocurrió un error inesperado al listar sus cursos: {e}")
        return redirect('mi_admin:dashboard_docente')


@login_required
@user_passes_test(is_docente, login_url='/')
def listar_estudiantes_por_curso_docente(request, curso_id):
    print(f"DEBUG (listar_estudiantes): Solicitud recibida para curso_id: {curso_id}")
    logger.debug(f"[{request.user.username}] DEBUG (listar_estudiantes): Solicitud recibida para curso_id: {curso_id}")

    curso = get_object_or_404(Curso, id=curso_id)
    curso.display_name = f"{curso.grado} '{curso.paralelo}' - {curso.get_niveles_display()}" 
    print(f"DEBUG (listar_estudiantes): Curso encontrado: {curso.display_name} (ID: {curso.id})")
    logger.debug(f"[{request.user.username}] DEBUG (listar_estudiantes): Curso encontrado: {curso.display_name} (ID: {curso.id})")

    estudiantes = Estudiante.objects.filter(curso_actual=curso).order_by('persona__apellidos', 'persona__nombres')
    
    print(f"DEBUG (listar_estudiantes): SQL de la consulta de estudiantes: {estudiantes.query}")
    logger.debug(f"[{request.user.username}] DEBUG (listar_estudiantes): SQL de la consulta de estudiantes: {estudiantes.query}")
    print(f"DEBUG (listar_estudiantes): Estudiantes encontrados por la consulta: {list(estudiantes)}")
    logger.debug(f"[{request.user.username}] DEBUG (listar_estudiantes): Estudiantes encontrados por la consulta: {list(estudiantes)}")
    
    if estudiantes.exists():
        first_estudiante = estudiantes.first()
        print(f"DEBUG (listar_estudiantes): Primer estudiante: {first_estudiante.persona.nombres} {first_estudiante.persona.apellidos} (ID: {first_estudiante.id})")
        logger.debug(f"[{request.user.username}] DEBUG (listar_estudiantes): Primer estudiante: {first_estudiante.persona.nombres} {first_estudiante.persona.apellidos} (ID: {first_estudiante.id})")
    else:
        print(f"DEBUG (listar_estudiantes): No se encontraron estudiantes para el curso {curso.id}.")
        logger.debug(f"[{request.user.username}] DEBUG (listar_estudiantes): No se encontraron estudiantes para el curso {curso.id}.")

    context = {
        'curso': curso,
        'estudiantes': estudiantes,
    }
    return render(request, 'mi_admin/listar_estudiantes_por_curso_docente.html', context)

@login_required
def registrar_asistencia(request, curso_id):
    docente = get_object_or_404(Docente, persona__usuario=request.user)
    curso = get_object_or_404(Curso, id=curso_id)
    asignaciones = Asignacion.objects.filter(docente=docente, curso=curso)
    
    today = date.today()
    trimestres = Trimestre.objects.filter(fecha_inicio__lte=today, fecha_fin__gte=today)
    
    trimestre_seleccionado_id = request.GET.get('trimestre_id')
    asignacion_seleccionada_id = request.GET.get('asignacion_id')

    estudiantes = []
    fechas_registradas = []
    asistencias_existentes = {}
    asistencia_hoy_pre_fill = {}
    selected_asignacion_obj = None
    trimestre_seleccionado = None
    asistencias_dict = {}
    faltas_dict = {}

    if request.method == 'POST':
        trimestre_id = request.POST.get('trimestre_id')
        asignacion_id = request.POST.get('asignacion_id')
        asignacion = get_object_or_404(Asignacion, id=asignacion_id)
        trimestre = get_object_or_404(Trimestre, id=trimestre_id)
        
        Asistencia.objects.filter(asignacion=asignacion, fecha=today).delete()

        estudiantes = Estudiante.objects.filter(curso_actual=curso).order_by('persona__apellidos')
        
        for estudiante in estudiantes:
            asistencia_value = request.POST.get(f'asistencia_{estudiante.id}')
            asistio = asistencia_value == 'on'
            Asistencia.objects.create(
                estudiante=estudiante,
                asignacion=asignacion,
                trimestre=trimestre,
                fecha=today,
                asistio=asistio
            )

        messages.success(request, 'La asistencia ha sido guardada correctamente.')
        return redirect('mi_admin:registrar_asistencia', curso_id=curso_id)

    if trimestre_seleccionado_id and asignacion_seleccionada_id:
        selected_asignacion_obj = get_object_or_404(Asignacion, id=asignacion_seleccionada_id)
        trimestre_seleccionado = get_object_or_404(Trimestre, id=trimestre_seleccionado_id)
        
        estudiantes = Estudiante.objects.filter(curso_actual=curso).order_by('persona__apellidos')
        
        registros_asistencia = Asistencia.objects.filter(
            asignacion=selected_asignacion_obj,
            trimestre=trimestre_seleccionado
        ).select_related('estudiante')
        
        fechas_registradas = sorted(list(registros_asistencia.values_list('fecha', flat=True).distinct()))
        fechas_registradas = [f.isoformat() for f in fechas_registradas]

        asistencias_existentes = {
            estudiante.id: {
                registro.fecha.isoformat(): registro.asistio
                for registro in registros_asistencia
                if registro.estudiante_id == estudiante.id
            }
            for estudiante in estudiantes
        }
        
        asistencia_hoy_pre_fill = {
            registro.estudiante_id: registro.asistio
            for registro in registros_asistencia.filter(fecha=today)
        }
        
        asistencias_dict = {}
        faltas_dict = {}
        for estudiante in estudiantes:
            total_asistencias = registros_asistencia.filter(estudiante=estudiante, asistio=True).count()
            total_faltas = registros_asistencia.filter(estudiante=estudiante, asistio=False).count()
            asistencias_dict[estudiante.id] = total_asistencias
            faltas_dict[estudiante.id] = total_faltas

    context = {
        'curso': curso,
        'trimestres': trimestres,
        'asignaciones': asignaciones,
        'estudiantes': estudiantes,
        'trimestre_seleccionado': trimestre_seleccionado,
        'selected_asignacion_obj': selected_asignacion_obj,
        'selected_asignacion_id': asignacion_seleccionada_id,
        'fechas_registradas': fechas_registradas,
        'asistencias_existentes': asistencias_existentes,
        'asistencia_hoy_pre_fill': asistencia_hoy_pre_fill,
        'today': today.isoformat(),
        'asistencias_dict': asistencias_dict,
        'faltas_dict': faltas_dict,
    }
    return render(request, 'mi_admin/asistencia.html', context)
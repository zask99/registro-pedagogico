from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
import json
from django.utils import timezone
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)

# Asegúrate de que estas importaciones sean correctas para tu estructura de modelos y formularios
from ..models import Materia, Docente, Asignacion, Curso, Persona
from ..forms import MateriaForm, AsignacionDocenteForm, AsignacionMateriaDocenteForm
# Función para verificar si el usuario es administrador
def es_admin(user):
    return user.is_authenticated and user.is_staff # O tu lógica para verificar el rol de administrador

@login_required
@user_passes_test(es_admin)
def materias_list_view(request):
    """
    Muestra una lista de materias y proporciona formularios para añadir nuevas materias
    y asignar docentes.
    """
    materias = Materia.objects.all().order_by('nombre')
    form_materia = MateriaForm()
    form_asignacion_docente = AsignacionDocenteForm()
    current_year = timezone.now().year

    context = {
        'materias': materias,
        'form_materia': form_materia,
        'form_asignacion_docente': form_asignacion_docente,
        'current_year': current_year,
    }
    return render(request, 'mi_admin/admin_lista_materias.html', context)

@login_required
@user_passes_test(es_admin)
@require_POST
def materias_create_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            form = MateriaForm(data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Materia creada exitosamente!')
                logger.info(f"[{request.user.username}] Materia '{form.cleaned_data['nombre']}' creada exitosamente.")
                return JsonResponse({'success': True, 'message': 'Materia creada exitosamente!'})
            else:
                logger.warning(f"[{request.user.username}] Errores de validación al crear materia: {form.errors.as_json()}")
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            logger.error(f"[{request.user.username}] JSONDecodeError en materias_create_view: Request body no es JSON válido.")
            return JsonResponse({'success': False, 'message': 'Invalid JSON format in request body.'}, status=400)
        except Exception as e:
            logger.exception(f"[{request.user.username}] Error inesperado al crear materia: {e}")
            return JsonResponse({'success': False, 'message': 'Ocurrió un error inesperado al crear la materia.'}, status=500)
    else:
        messages.error(request, 'Acceso inválido al crear materia.')
        return redirect('mi_admin:admin_materias_list')


@login_required
@user_passes_test(es_admin, login_url='/')
def assign_teacher_view(request):
    
    # Si la solicitud es POST
    if request.method == 'POST':
        
        # ---------------------------------------------------------------
        # 1. MANEJO DE AJAX (Desde el modal de la lista de materias)
        # Esta parte usa AsignacionDocenteForm (con el hidden field)
        # ---------------------------------------------------------------
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                form_data = {
                    'materia_id': data.get('materia_id'),
                    'curso': data.get('curso'),
                    'docente': data.get('docente'),
                    'anio_academico': data.get('anio_academico'),
                }
                form = AsignacionDocenteForm(form_data) # Formulario con hidden field
                
                if form.is_valid():
                    materia_id = form.cleaned_data['materia_id']
                    
                    # --- MEJORA: Usar get_object_or_404 ---
                    # Esto previene el error DoesNotExist y maneja IDs nulos
                    materia = get_object_or_404(Materia, id=materia_id)
                    # --- FIN MEJORA ---

                    curso = form.cleaned_data['curso']
                    docente = form.cleaned_data['docente']
                    anio = form.cleaned_data['anio_academico']

                    Asignacion.objects.create(
                        materia=materia, curso=curso, docente=docente, anio_academico=anio
                    )
                    messages.success(request, 'Docente asignado exitosamente a la materia y curso.')
                    logger.info(f"[{request.user.username}] Docente {docente.persona.nombres} {docente.persona.apellidos} asignado a Materia {materia.nombre}, Curso {curso.get_full_name()}, Año {anio}.")
                    return JsonResponse({'success': True, 'message': 'Docente asignado exitosamente.'})
                else:
                    logger.warning(f"[{request.user.username}] Errores de validación al asignar docente (AJAX): {form.errors.as_json()}")
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            except json.JSONDecodeError:
                logger.error(f"[{request.user.username}] JSONDecodeError en assign_teacher_view.")
                return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
            except Http404:
                logger.warning(f"[{request.user.username}] Se intentó asignar docente a materia inexistente (AJAX).")
                return JsonResponse({'success': False, 'message': 'La materia especificada no existe.'}, status=404)
            except Exception as e:
                logger.exception(f"[{request.user.username}] Error inesperado al asignar docente (AJAX): {e}")
                return JsonResponse({'success': False, 'message': 'Ocurrió un error inesperado.'}, status=500)

        # ---------------------------------------------------------------
        # 2. MANEJO DE POST HTML (Desde la página /materias/assign_teacher/)
        # Esta parte AHORA usa AsignacionMateriaDocenteForm (el ModelForm)
        # ---------------------------------------------------------------
        else:
            # !! CORRECCIÓN: Usar AsignacionMateriaDocenteForm !!
            form = AsignacionMateriaDocenteForm(request.POST) 
            
            if form.is_valid():
                # !! CORRECCIÓN: Este formulario SÍ tiene .save() !!
                form.save() 
                
                messages.success(request, 'Asignación creada exitosamente.')
                return redirect('mi_admin:admin_materias_list') # Redirige a la lista
            else:
                messages.error(request, "Error al crear la asignación. Por favor, revise los datos.")
                # El flujo continúa para renderizar la página con el formulario y sus errores

    # ---------------------------------------------------------------
    # 3. MANEJO DE GET (Mostrar la página /materias/assign_teacher/)
    # ---------------------------------------------------------------
    else:
        # !! CORRECCIÓN: Usar AsignacionMateriaDocenteForm !!
        form = AsignacionMateriaDocenteForm() 

    # Renderiza la plantilla, pasando el formulario
    # (ya sea el 'form' vacío del GET o el 'form' con errores del POST)
    return render(request, 'mi_admin/admin_assign_teacher.html', {'form': form})




@login_required
@user_passes_test(es_admin)
def api_get_materia_assignments(request, materia_id):
    """
    API endpoint para obtener asignaciones existentes para una materia específica y un año opcional.
    Devuelve JSON.
    """
    try:
        materia = get_object_or_404(Materia, id=materia_id)
    except Http404:
        logger.warning(f"[{request.user.username}] Materia con ID {materia_id} no encontrada para API de asignaciones.")
        return JsonResponse([], status=404)

    assignments = Asignacion.objects.filter(materia=materia)

    anio_academico_str = request.GET.get('anio')
    if anio_academico_str:
        try:
            anio_academico = int(anio_academico_str)
            assignments = assignments.filter(anio_academico=anio_academico)
        except ValueError:
            logger.warning(f"[{request.user.username}] Valor de año académico inválido '{anio_academico_str}' en api_get_materia_assignments.")
            # Si el año es inválido, simplemente no se filtra por año.

    # Optimizar la consulta usando select_related para traer los datos del curso y docente (y su persona)
    assignments = assignments.select_related('curso', 'docente', 'docente__persona').order_by('anio_academico', 'curso__grado', 'curso__paralelo')

    data = []
    for asig in assignments:
        docente_nombre = "N/A"
        if asig.docente and asig.docente.persona:
            docente_nombre = f"{asig.docente.persona.nombres} {asig.docente.persona.apellidos}"
        elif asig.docente:
             # Fallback if persona somehow doesn't exist for a docente, though it should
            docente_nombre = f"Docente ID: {asig.docente.id}"

        curso_nombre = "N/A"
        if asig.curso:
            # Asumiendo que tu modelo Curso tiene un método get_full_name()
            if hasattr(asig.curso, 'get_full_name'):
                curso_nombre = asig.curso.get_full_name()
            else:
                # Si no existe get_full_name, construirlo
                curso_nombre = f"{asig.curso.grado} '{asig.curso.paralelo}' ({asig.curso.niveles})"

        data.append({
            'id': asig.id,
            'curso_id': asig.curso.id if asig.curso else None,
            'curso_nombre': curso_nombre,
            'docente_id': asig.docente.id if asig.docente else None,
            'docente_nombre': docente_nombre,
            'anio_academico': asig.anio_academico,
        })
    return JsonResponse(data, safe=False)
# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\views\admin_gestion_curso_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Importaciones combinadas y limpias
from ..forms import CursoForm, AsignacionForm 
from ..models import Curso, Asignacion

# Función de verificación de rol
def es_admin(user):
    # Asegúrate que el nombre coincida con tu BD (usando .lower().strip() es más seguro)
    return user.is_authenticated and hasattr(user, 'rol') and user.rol and user.rol.nombre.lower().strip() == 'administrativo'


@login_required
@user_passes_test(es_admin)
def admin_assign_materia_to_curso(request):
    """
    Vista para asignar una materia y docente a un curso específico.
    Maneja la visualización del formulario (GET) y el procesamiento (POST).
    """
    curso_id = request.GET.get('curso_id')
    curso_seleccionado = None
    if curso_id:
        try:
            curso_seleccionado = Curso.objects.get(pk=curso_id)
        except Curso.DoesNotExist:
            messages.error(request, 'El curso especificado no existe.')
            return redirect('mi_admin:admin_listar_cursos') # Redirige si el curso no se encuentra

    if request.method == 'POST':
        form = AsignacionForm(request.POST)
        if form.is_valid():
            asignacion = form.save(commit=False)
            
            if curso_seleccionado:
                 asignacion.curso = curso_seleccionado
            
            asignacion.save()
            messages.success(request, f'Materia asignada exitosamente al curso {asignacion.curso}.')
            return redirect('mi_admin:admin_listar_cursos') # Vuelve a la lista de cursos
        else:
            messages.error(request, 'Error al asignar la materia. Revise los datos.')
    else: # GET request
        initial_data = {}
        if curso_seleccionado:
            initial_data['curso'] = curso_seleccionado.id # Pasa el ID del curso para preseleccionar

        form = AsignacionForm(initial=initial_data)

    context = {
        'form': form,
        'curso_seleccionado': curso_seleccionado,
    }
    return render(request, 'mi_admin/admin_assign_assignment_form.html', context)

@login_required
@user_passes_test(es_admin)
def admin_anadir_curso(request):
    """
    Vista para añadir un nuevo curso al sistema.
    Permite a los administradores registrar nuevos cursos a través de un formulario.
    """
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Curso añadido exitosamente!')
            return redirect('mi_admin:admin_listar_cursos') # Redirige a la lista de cursos
        else:
            messages.error(request, 'Hubo un error al añadir el curso. Por favor, revisa los datos.')
    else:
        form = CursoForm() # Crea un formulario vacío para GET request

    context = {
        'form': form,
        'titulo': 'Añadir Nuevo Curso'
    }
    return render(request, 'mi_admin/admin_anadir_curso.html', context)
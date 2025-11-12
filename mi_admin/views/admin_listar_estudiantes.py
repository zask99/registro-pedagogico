# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\views\admin_listar_estudiantes.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Importamos el modelo 'Inscripcion' que es el que ahora une a Estudiantes y Cursos
from mi_admin.models import Curso, Inscripcion
from django.contrib import messages


@login_required
def admin_listar_estudiantes(request, curso_id):
    """
    Vista para listar los estudiantes inscritos en un curso específico.
    """
    curso = get_object_or_404(Curso, id=curso_id)

    # --- ESTA CONSULTA YA ES CORRECTA ---
    # Trae Inscripcion, Estudiante y Persona en un solo viaje a la BD.
    inscripciones = Inscripcion.objects.filter(curso=curso).select_related(
        'estudiante', 
        'estudiante__persona'
    ).order_by(
        'estudiante__persona__apellidos', 
        'estudiante__persona__nombres'
    )
    # --- FIN DE LA CONSULTA ---

    context = {
        'curso': curso,
        'inscripciones': inscripciones, # Pasamos las inscripciones, que contienen todo
    }
    
    return render(request, 'mi_admin/admin_listar_estudiantes.html', context)
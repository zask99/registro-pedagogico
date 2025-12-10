# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\views\admin_admin_listar_curso.py
# (O donde sea que tengas definida la vista admin_listar_curso)

from django.shortcuts import render
from mi_admin.models import Curso # Onde sea que estén tus modelos

def admin_listar_curso(request):
    cursos = Curso.objects.all().order_by('niveles', 'grado', 'paralelo') # Añadí ordenación para consistencia
    # ¡Asegúrate que esta ruta a la plantilla sea correcta!
    return render(request, 'mi_admin/admin_listar_curso.html', {'cursos': cursos})
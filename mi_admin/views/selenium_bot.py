from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required

# Importa tus modelos de 'models.py'
from mi_admin.models import Curso, Materia, Trimestre, Asignacion, ResumenTrimestral

# Importa tu tarea de Celery
from mi_admin.tasks import iniciar_subida_sie_task 

# 
# TU VISTA EXISTENTE (SIN CAMBIOS)
#
class CargarNotasSIEView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    template_name = 'mi_admin/admin_cargar_notas_sie.html'
    
    def test_func(self):
        # Asegura que solo el admin (o staff) pueda ver esta página
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        """
        GET: Muestra el formulario con los menús desplegables.
        """
        context = {
            'cursos': Curso.objects.all().order_by('grado', 'paralelo'),
            'materias': Materia.objects.all().order_by('nombre'),
            'trimestres': Trimestre.objects.all().order_by('-gestion', '-numero'),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        POST: El admin presionó "Iniciar Carga".
        """
        
        # 1. Obtenemos los datos del formulario
        trimestre_id = request.POST.get('trimestre')
        curso_id = request.POST.get('curso')
        materia_id = request.POST.get('materia')
        
        # 2. Obtenemos las credenciales (¡nunca las guardes!)
        username_sie = request.POST.get('username_sie')
        password_sie = request.POST.get('password_sie')

        # 3. Lanzar la tarea de fondo (Celery)
        iniciar_subida_sie_task.delay(
            trimestre_id=trimestre_id,
            curso_id=curso_id,
            materia_id=materia_id,
            username_sie=username_sie,
            password_sie=password_sie
        )
        
        # 5. Redirigir al admin al dashboard con un mensaje
        messages.success(request, '¡Carga iniciada! El proceso se está ejecutando en segundo plano.')
        
        return redirect('mi_admin:main_dashboard') 


# =======================================================
# NUEVA VISTA: Añade esta función a tu archivo
# =======================================================
@login_required
@staff_member_required
@require_GET  # Solo permite peticiones GET
def ajax_preview_notas_view(request):
    """
    Esta vista responde a la llamada AJAX para previsualizar notas.
    Devuelve los datos en formato JSON.
    """
    trimestre_id = request.GET.get('trimestre_id')
    curso_id = request.GET.get('curso_id')
    materia_id = request.GET.get('materia_id')

    if not all([trimestre_id, curso_id, materia_id]):
        return JsonResponse({'error': 'Faltan parámetros (trimestre, curso o materia).'}, status=400)

    try:
        # 1. Encontrar la asignación
        asignacion = Asignacion.objects.get(curso_id=curso_id, materia_id=materia_id)
        
        # 2. Obtener las notas (ResumenTrimestral)
        resumenes = ResumenTrimestral.objects.filter(
            asignacion=asignacion,
            trimestre_id=trimestre_id
        ).select_related(
            'estudiante__persona' # Optimiza la consulta para incluir datos de persona
        ).order_by(
            'estudiante__persona__apellidos', 
            'estudiante__persona__nombres'
        )

        if not resumenes.exists():
            return JsonResponse({'error': 'No se encontraron notas registradas para esta selección.'}, status=404)

        # 3. Preparar los datos para JSON
        lista_de_notas = []
        for res in resumenes:
            lista_de_notas.append({
                'nombre_estudiante': res.estudiante.persona.get_full_name(),
                'ci_estudiante': res.estudiante.persona.ci,
                'nota_final': res.nota_final_trimestre,
            })

        return JsonResponse({'notas': lista_de_notas})

    except Asignacion.DoesNotExist:
        return JsonResponse({'error': 'La combinación de curso y materia no existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error interno del servidor: {str(e)}'}, status=500)
# mi_admin/views/selenium_bot.py

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required

# Importa tus modelos
from mi_admin.models import Curso, Materia, Trimestre, Asignacion, ResumenTrimestral
# Importa tu tarea de Celery
from mi_admin.tasks import iniciar_subida_sie_task 

class CargarNotasSIEView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'mi_admin/admin_cargar_notas_sie.html'
    
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        context = {
            'cursos': Curso.objects.all().order_by('grado', 'paralelo'),
            'materias': Materia.objects.all().order_by('nombre'),
            'trimestres': Trimestre.objects.all().order_by('-gestion', '-numero'),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        MODIFICADO: Ahora devuelve JSON para que la página no se recargue.
        """
        # 1. Datos del formulario
        trimestre_id = request.POST.get('trimestre')
        curso_id = request.POST.get('curso')
        materia_id = request.POST.get('materia')
        username_sie = request.POST.get('username_sie')
        password_sie = request.POST.get('password_sie')

        # Validaciones básicas
        if not all([trimestre_id, curso_id, materia_id, username_sie, password_sie]):
             return JsonResponse({'status': 'error', 'message': 'Faltan datos obligatorios.'}, status=400)

        # 2. Lanzar Celery
        iniciar_subida_sie_task.delay(
            trimestre_id=trimestre_id,
            curso_id=curso_id,
            materia_id=materia_id,
            username_sie=username_sie,
            password_sie=password_sie
        )
        
        # 3. Respuesta JSON (El JS se encarga de mostrar el mensaje)
        return JsonResponse({
            'status': 'success', 
            'message': '¡Conectando con el bot! La carga se realizará en segundo plano.'
        })


@login_required
@staff_member_required
@require_GET
def ajax_preview_notas_view(request):
    """
    MODIFICADO: Corregido el error de 'ci' vs 'carnet'.
    """
    trimestre_id = request.GET.get('trimestre_id')
    curso_id = request.GET.get('curso_id')
    materia_id = request.GET.get('materia_id')

    if not all([trimestre_id, curso_id, materia_id]):
        return JsonResponse({'error': 'Faltan parámetros.'}, status=400)

    try:
        asignacion = Asignacion.objects.get(curso_id=curso_id, materia_id=materia_id)
        
        resumenes = ResumenTrimestral.objects.filter(
            asignacion=asignacion,
            trimestre_id=trimestre_id
        ).select_related('estudiante__persona').order_by('estudiante__persona__apellidos')

        if not resumenes.exists():
            return JsonResponse({'error': 'No hay notas registradas para esta selección.'}, status=404)

        lista_de_notas = []
        for res in resumenes:
            lista_de_notas.append({
                'nombre_estudiante': res.estudiante.persona.get_full_name(),
                # CORRECCIÓN AQUÍ: Usamos .carnet en lugar de .ci
                'ci_estudiante': res.estudiante.persona.carnet, 
                'nota_final': res.nota_final_trimestre,
            })

        return JsonResponse({'notas': lista_de_notas})

    except Asignacion.DoesNotExist:
        return JsonResponse({'error': 'Esa materia no está asignada a este curso.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
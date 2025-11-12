from celery import shared_task
from mi_admin.models import Trimestre, Curso, Materia, Asignacion, ResumenTrimestral
from .views.selenium_logic import ejecutar_bot_sie # El bot real

@shared_task(bind=True)
def iniciar_subida_sie_task(self, trimestre_id, curso_id, materia_id, username_sie, password_sie):
    try:
        # 1. Obtener la Asignación
        asignacion = Asignacion.objects.get(curso_id=curso_id, materia_id=materia_id)
        trimestre = Trimestre.objects.get(id=trimestre_id)

        # 2. Obtener las notas de tu BD
        notas_para_subir = ResumenTrimestral.objects.filter(
            asignacion=asignacion,
            trimestre=trimestre
        ).order_by('estudiante__persona__apellidos')
        
        if not notas_para_subir.exists():
            return "No se encontraron notas para subir con esos filtros."

        # 3. Preparar datos simples para el bot
        datos_simples = [
            {
                'ci': res.estudiante.persona.ci,
                'nombre': res.estudiante.persona.get_full_name(),
                'nota_final': res.nota_final_trimestre 
            }
            for res in notas_para_subir
        ]

        # 4. Llamar al bot de Selenium
        resultado = ejecutar_bot_sie(
            username=username_sie,
            password=password_sie,
            notas=datos_simples,
            # Pasa los nombres para que el bot pueda buscar
            curso_nombre=asignacion.curso.get_full_name(),
            materia_nombre=asignacion.materia.nombre
        )
        return f"Éxito: {resultado}"
    except Exception as e:
        return f"Error: {e}"
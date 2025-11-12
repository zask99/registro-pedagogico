import io
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Prefetch, Sum, F
from decimal import Decimal
from mi_admin.models import (
    Asignacion, Trimestre, TipoComponente, Subcomponente, Evaluacion,
    Inscripcion, ResumenTrimestral, Nota
)
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    """Función de utilidad para renderizar un PDF."""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def obtener_rango_nota(nota):
    """Función auxiliar para obtener el rango cualitativo de una nota."""
    if nota is None:
        return 'N/A'
    if nota >= 90:
        return 'DP'  # Desarrollo Pleno
    elif nota >= 70:
        return 'DO'  # Desarrollo Óptimo
    elif nota >= 60:
        return 'DA'  # Desarrollo Adecuado
    else:
        return 'ED'  # En Desarrollo


def reporte_asignacion_trimestre_pdf(request):
    """
    Vista que genera el reporte de notas trimestral,
    con lógica optimizada y corrección de capitalización.
    """
    asignacion_id = request.GET.get('asignacion')
    trimestre_id = request.GET.get('trimestre')

    if not asignacion_id or not trimestre_id:
        return HttpResponse("Faltan los parámetros 'asignacion' o 'trimestre'.", status=400)

    try:
        asignacion = get_object_or_404(Asignacion, id=asignacion_id)
        trimestre = get_object_or_404(Trimestre, id=trimestre_id)

        saber_comp_qs = TipoComponente.objects.filter(nombre='Saber')
        hacer_comp_qs = TipoComponente.objects.filter(nombre='Hacer')
        ser_comp_qs = TipoComponente.objects.filter(nombre='Ser')
        decidir_comp_qs = TipoComponente.objects.filter(nombre='Decidir')
        
        saber_comp = saber_comp_qs.first()
        hacer_comp = hacer_comp_qs.first()
        ser_comp = ser_comp_qs.first()
        decidir_comp = decidir_comp_qs.first()

    except (Asignacion.DoesNotExist, Trimestre.DoesNotExist):
        return HttpResponse("Error: Los objetos Asignacion o Trimestre no existen.", status=404)
    
    subcomponentes_saber = Subcomponente.objects.filter(
        asignacion=asignacion,
        trimestre=trimestre,
        tipo_componente=saber_comp
    )
    
    subcomponentes_hacer = Subcomponente.objects.filter(
        asignacion=asignacion,
        trimestre=trimestre,
        tipo_componente=hacer_comp
    )
    
    evaluaciones_saber = Evaluacion.objects.filter(
        subcomponente__in=subcomponentes_saber
    ).order_by('nombre')
    
    evaluaciones_hacer = Evaluacion.objects.filter(
        subcomponente__in=subcomponentes_hacer
    ).order_by('nombre')
    
    total_ponderacion_saber = sum(eval.ponderacion for eval in evaluaciones_saber)
    total_ponderacion_hacer = sum(eval.ponderacion for eval in evaluaciones_hacer)

    inscripciones = Inscripcion.objects.filter(
        curso=asignacion.curso,
        anio_academico=asignacion.anio_academico
    ).select_related(
        'estudiante__persona'
    ).prefetch_related(
        Prefetch(
            'estudiante__nota_set',
            queryset=Nota.objects.filter(
                evaluacion__in=list(evaluaciones_saber) + list(evaluaciones_hacer)
            ).select_related('evaluacion')
        ),
        Prefetch(
            'estudiante__resumentrimestral_set',
            queryset=ResumenTrimestral.objects.filter(
                asignacion=asignacion,
                trimestre=trimestre
            )
        )
    ).order_by('estudiante__persona__apellidos')
    
    estudiantes_con_notas = []
    
    for inscripcion in inscripciones:
        estudiante = inscripcion.estudiante
        
        notas_dict = {
            nota.evaluacion.id: nota.nota_obtenida
            for nota in estudiante.nota_set.all()
        }
        
        resumen_trimestral, created = ResumenTrimestral.objects.get_or_create(
            estudiante=estudiante,
            asignacion=asignacion,
            trimestre=trimestre
        )

        nota_saber_calculada = sum(notas_dict.get(eval.id, Decimal('0.00')) for eval in evaluaciones_saber)
        nota_hacer_calculada = sum(notas_dict.get(eval.id, Decimal('0.00')) for eval in evaluaciones_hacer)
        
        nota_saber = resumen_trimestral.nota_saber if resumen_trimestral.nota_saber is not None else nota_saber_calculada
        nota_hacer = resumen_trimestral.nota_hacer if resumen_trimestral.nota_hacer is not None else nota_hacer_calculada
        nota_ser = resumen_trimestral.nota_ser
        nota_decidir = resumen_trimestral.nota_decidir
        nota_final = resumen_trimestral.nota_final_trimestre
        rango = resumen_trimestral.rango
        
        # Nuevos campos del ResumenTrimestral
        situacion = resumen_trimestral.situacion
        autoeval = resumen_trimestral.autoeval

        estudiantes_con_notas.append({
            'estudiante': estudiante,
            'ci': estudiante.persona.ci,
            'notas_evaluaciones': notas_dict,
            'nota_saber': nota_saber,
            'nota_hacer': nota_hacer,
            'nota_ser': nota_ser,
            'nota_decidir': nota_decidir,
            'nota_final_trimestre': nota_final,
            'rango': rango,
            'situacion': situacion,
            'autoeval': autoeval
        })

    if not estudiantes_con_notas:
        return HttpResponse("No hay estudiantes inscritos o notas registradas para este trimestre.", status=404)
    
    PUNTAJE_MAXIMO_COMPONENTE = {
        'SABER': saber_comp.porcentaje_total_componente if saber_comp else Decimal(35.0),
        'HACER': hacer_comp.porcentaje_total_componente if hacer_comp else Decimal(35.0),
        'SER': ser_comp.porcentaje_total_componente if ser_comp else Decimal(15.0),
        'DECIDIR': decidir_comp.porcentaje_total_componente if decidir_comp else Decimal(15.0),
    }

    context = {
        'asignacion': asignacion,
        'trimestre': trimestre,
        'evaluaciones_saber': evaluaciones_saber,
        'evaluaciones_hacer': evaluaciones_hacer,
        'subcomponentes_saber': subcomponentes_saber,
        'subcomponentes_hacer': subcomponentes_hacer,
        'total_ponderacion_saber': total_ponderacion_saber,
        'total_ponderacion_hacer': total_ponderacion_hacer,
        'estudiantes_con_notas': estudiantes_con_notas,
        'fecha_generacion_reporte': datetime.datetime.now(),
        'PUNTAJE_MAXIMO_COMPONENTE': PUNTAJE_MAXIMO_COMPONENTE,
    }
    
    return render_to_pdf('mi_admin/docente_reporte_asignacion_trimestre_pdf.html', context)
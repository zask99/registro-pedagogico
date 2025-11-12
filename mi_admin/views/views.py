# mi_admin/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch, Count
from decimal import Decimal, InvalidOperation
from datetime import date
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST

from mi_admin.models import (
    Docente, Asignacion, Trimestre, Estudiante, Nota, Evaluacion, Subcomponente, Persona,
    TipoComponente, ResumenTrimestral, Asistencia, Materia
)

@csrf_exempt
@require_POST
def crear_evaluacion(request):
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre')
        ponderacion = data.get('ponderacion')
        subcomponente_id = data.get('subcomponente_id')
        asignacion_id = data.get('asignacion_id')
        trimestre_id = data.get('trimestre_id')

        # Aquí iría tu lógica para crear la nueva evaluación
        # Por ejemplo, instanciar y guardar un objeto de tu modelo Evaluacion

        return JsonResponse({'status': 'success', 'message': 'Evaluación creada exitosamente.'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
@require_POST
def guardar_desempeno(request):
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        asignacion_id = data.get('asignacion_id')
        trimestre_id = data.get('trimestre_id')
        observacion_texto = data.get('observacion_texto')
        rango_cualitativo = data.get('rango_cualitativo')

        # Aquí iría tu lógica para guardar el desempeño
        return JsonResponse({'status': 'success', 'message': 'Desempeño guardado exitosamente.'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# Helper function
def _recalcular_promedio_final_trimestral(estudiante, asignacion, trimestre):
    """
    Recalcula el promedio final trimestral de un estudiante para una asignación y trimestre dados.
    Esta función debe actualizar el campo nota_final_trimestre en el ResumenTrimestral.
    """
    try:
        resumen = ResumenTrimestral.objects.get(
            estudiante=estudiante,
            asignacion=asignacion,
            trimestre=trimestre
        )

        # Retrieve scores, defaulting to 0.00 if None for calculation
        nota_saber = resumen.nota_saber if resumen.nota_saber is not None else Decimal('0.00')
        nota_hacer = resumen.nota_hacer if resumen.nota_hacer is not None else Decimal('0.00')
        nota_ser = resumen.nota_ser if resumen.nota_ser is not None else Decimal('0.00')
        nota_decidir = resumen.nota_decidir if resumen.nota_decidir is not None else Decimal('0.00')
        autoeval = resumen.autoeval if resumen.autoeval is not None else Decimal('0.00')


        # Calculate the sum of the four components (Saber, Hacer, Ser, Decidir) and Autoevaluación
        # Assuming Autoeval also contributes directly to the final grade as per usage in guardar_autoevaluacion
        final_grade = (nota_saber + nota_hacer + nota_ser + nota_decidir + autoeval).quantize(Decimal('0.01'))

        resumen.nota_final_trimestre = final_grade
        resumen.save()
        return final_grade
    except ResumenTrimestral.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error recalculating final trimester average: {e}")
        return None


@login_required
def docente_calificaciones_view(request):
    asignacion_id = request.GET.get('asignacion')
    trimestre_id = request.GET.get('trimestre')
    docente_persona = request.user.persona
    docente = get_object_or_404(Docente, persona=docente_persona)
    print(f"DEBUG: asignacion_id obtenido: {asignacion_id}")
    print(f"DEBUG: trimestre_id obtenido: {trimestre_id}")

    asignaciones = Asignacion.objects.filter(docente=docente).select_related(
        'curso', 'materia'
    ).order_by('curso__grado', 'curso__paralelo', 'materia__nombre')

    trimestres = Trimestre.objects.all().order_by('gestion', 'numero')

    selected_asignacion_id = request.GET.get('asignacion', None)
    selected_trimestre_id = request.GET.get('trimestre', None)

    estudiantes_data = []
    selected_asignacion = None
    selected_trimestre = None
    evaluaciones_saber = []
    evaluaciones_hacer = []

    if selected_asignacion_id and selected_trimestre_id:
        selected_asignacion = get_object_or_404(Asignacion, id=selected_asignacion_id, docente=docente)
        selected_trimestre = get_object_or_404(Trimestre, id=selected_trimestre_id)

        # Solo carga evaluaciones para Saber y Hacer (las que tienen notas individuales)
        all_evaluaciones = Evaluacion.objects.filter(
            asignacion=selected_asignacion,
            trimestre=selected_trimestre,
            subcomponente__tipo_componente__nombre__in=['Saber', 'Hacer'] # Filtra por los tipos que usan evaluaciones
        ).select_related('subcomponente', 'subcomponente__tipo_componente', 'asignacion', 'trimestre') \
         .order_by('subcomponente__tipo_componente__nombre', 'id')

        for eval_obj in all_evaluaciones:
            eval_data = {
                'id': eval_obj.id,
                'nombre': eval_obj.nombre,
                'ponderacion': eval_obj.ponderacion,
                'note_key': f"{eval_obj.subcomponente.tipo_componente.nombre.lower()}_eval_{eval_obj.id}"
            }
            if eval_obj.subcomponente.tipo_componente.nombre.lower() == 'saber':
                evaluaciones_saber.append(eval_data)
            elif eval_obj.subcomponente.tipo_componente.nombre.lower() == 'hacer':
                evaluaciones_hacer.append(eval_data)


        estudiantes = Estudiante.objects.filter(
            curso_actual=selected_asignacion.curso
        ).distinct().select_related('persona').order_by('persona__apellidos', 'persona__nombres')

        notes_prefetch = Prefetch(
            'nota_set',
            queryset=Nota.objects.filter(evaluacion__in=all_evaluaciones).select_related('evaluacion__subcomponente__tipo_componente'),
            to_attr='_prefetched_notes'
        )

        resumen_prefetch = Prefetch(
            'resumentrimestral_set',
            queryset=ResumenTrimestral.objects.filter(
                asignacion=selected_asignacion,
                trimestre=selected_trimestre
            ),
            to_attr='_prefetched_resumenes'
        )

        estudiantes = estudiantes.prefetch_related(notes_prefetch, resumen_prefetch)

        total_class_days = Asistencia.objects.filter(
            asignacion=selected_asignacion,
            trimestre=selected_trimestre
        ).values('fecha').distinct().count()
        if total_class_days == 0:
            total_class_days_display = "N/A"
        else:
            total_class_days_display = str(total_class_days)

        attendance_counts_query = Asistencia.objects.filter(
            estudiante__in=estudiantes,
            asignacion=selected_asignacion,
            trimestre=selected_trimestre,
            asistio=True # <--- Esta línea estaba comentada. Asegura que solo se cuenten las asistencias.
        ).values('estudiante_id').annotate(
            conteo_asistencias=Count('id')
        )
        attendance_map = {item['estudiante_id']: item['conteo_asistencias'] for item in attendance_counts_query}


        for i, estudiante in enumerate(estudiantes):
            student_notes = {}
            for nota in estudiante._prefetched_notes:
                key = f"{nota.evaluacion.subcomponente.tipo_componente.nombre.lower()}_eval_{nota.evaluacion.id}"
                # Store notes as Decimal to maintain precision for calculations
                if nota.nota_obtenida is not None:
                    student_notes[key] = Decimal(str(nota.nota_obtenida))
                else:
                    student_notes[key] = None

            resumen_obj, resumen_created = ResumenTrimestral.objects.get_or_create(
                estudiante=estudiante,
                asignacion=selected_asignacion,
                trimestre=selected_trimestre
            )
            # Fetch existing DECIDIR, AUTOEVAL, SER values if they exist directly from resumen_obj
            nota_decidir = resumen_obj.nota_decidir
            autoeval = resumen_obj.autoeval
            observaciones = resumen_obj.observaciones
            # prom_ser = resumen_obj.nota_ser # Directamente del resumen, ya no es un promedio de evaluaciones


            # --- Weighted Average for Saber ---
            sum_weighted_saber = Decimal(0)
            total_ponderacion_saber = Decimal(0)
            for eval_saber_data in evaluaciones_saber:
                note_key = eval_saber_data['note_key']
                if note_key in student_notes and student_notes[note_key] is not None:
                    sum_weighted_saber += student_notes[note_key] * Decimal(str(eval_saber_data['ponderacion']))
                    total_ponderacion_saber += Decimal(str(eval_saber_data['ponderacion']))

            prom_saber = Decimal('0.00')
            if total_ponderacion_saber > 0:
                prom_saber = (sum_weighted_saber / total_ponderacion_saber).quantize(Decimal('0.01'))

            # --- Weighted Average for Hacer ---
            sum_weighted_hacer = Decimal(0)
            total_ponderacion_hacer = Decimal(0)
            for eval_hacer_data in evaluaciones_hacer:
                note_key = eval_hacer_data['note_key']
                if note_key in student_notes and student_notes[note_key] is not None:
                    sum_weighted_hacer += student_notes[note_key] * Decimal(str(eval_hacer_data['ponderacion']))
                    total_ponderacion_hacer += Decimal(str(eval_hacer_data['ponderacion']))

            prom_hacer = Decimal('0.00')
            if total_ponderacion_hacer > 0:
                prom_hacer = (sum_weighted_hacer / total_ponderacion_hacer).quantize(Decimal('0.01'))

            # NO SE CALCULA MAS PROMEDIO PONDERADO PARA 'SER', SE OBTIENE DIRECTAMENTE DEL RESUMEN
            # prom_ser ya se obtuvo de resumen_obj.nota_ser

            # --- Attendance Display and Score Calculation ---
            asistencia_actual = attendance_map.get(estudiante.id, 0)
            asistencia_nota_sobre_10 = None

            if total_class_days > 0:
                if asistencia_actual > 0:
                    asistencia_percentage = (Decimal(asistencia_actual) / Decimal(total_class_days)) * 100
                    asistencia_display = f"{asistencia_percentage:.2f}% ({asistencia_actual}/{total_class_days_display})"
                    asistencia_nota_sobre_10 = (asistencia_percentage / Decimal(10)).quantize(Decimal('0.01'))
                else:
                    asistencia_display = f"0.00% ({asistencia_actual}/{total_class_days_display})"
                    asistencia_nota_sobre_10 = None
            else:
                asistencia_display = "N/A (No hay clases registradas)"
                asistencia_nota_sobre_10 = None

            # *** MODIFICACIÓN SOLICITADA: Guardar nota de asistencia en nota_ser ***
            if asistencia_nota_sobre_10 is not None:
                resumen_obj.nota_ser = asistencia_nota_sobre_10
            else:
                resumen_obj.nota_ser = None # O Decimal('0.00') si prefieres un valor por defecto numérico.
            # ********************************************************************

            # Update resumen_obj with calculated Saber, Hacer and fetched Ser (now attendance), Decidir, Autoeval
            resumen_obj.nota_saber = prom_saber
            resumen_obj.nota_hacer = prom_hacer
            # resumen_obj.nota_ser ya se asignó arriba con la nota de asistencia
            resumen_obj.nota_decidir = nota_decidir # Ya cargado directamente
            resumen_obj.autoeval = autoeval # Ya cargado directamente
            resumen_obj.observaciones = observaciones

            # Save the component notes, autoeval, and observations first
            resumen_obj.save()

            # Recalculate the final trimester grade (nota_final_trimestre)
            # This function internally saves nota_final_trimestre
            _recalcular_promedio_final_trimestral(estudiante, selected_asignacion, selected_trimestre)
            resumen_obj.refresh_from_db() # Refresh resumen object to get the latest nota_final_trimestre

            # Use the refreshed nota_final_trimestre for situacion and for collecting data for rango
            final_grade_for_display = float(resumen_obj.nota_final_trimestre) if resumen_obj.nota_final_trimestre is not None else None


            # --- Situation Calculation and Assignment ---
            situacion_display = "N/A"
            if final_grade_for_display is not None:
                if final_grade_for_display >= 51:
                    situacion_display = "Aprobado"
                else:
                    situacion_display = "Reprobado"

            # Asigna y guarda la situación en la base de datos
            resumen_obj.situacion = situacion_display
            resumen_obj.save() # Guarda la situación inmediatamente


            estudiantes_data.append({
                'nro': i + 1,
                'id': estudiante.id,
                'nombre_completo': estudiante.persona.get_full_name(),
                'prom_saber': float(prom_saber) if prom_saber is not None else None,
                'prom_hacer': float(prom_hacer) if prom_hacer is not None else None,
                # 'nota_ser' ahora mostrará la nota de asistencia
                'nota_ser': float(resumen_obj.nota_ser) if resumen_obj.nota_ser is not None else None,
                'nota_decidir': float(nota_decidir) if nota_decidir is not None else None,
                'asistencia': asistencia_display,
                'asistencia_nota_sobre_10': float(asistencia_nota_sobre_10) if asistencia_nota_sobre_10 is not None else None,
                'observaciones': observaciones,
                'autoeval': float(autoeval) if autoeval is not None else None,
                'prom_trim': final_grade_for_display,
                'rango': "N/A",
                'situacion': situacion_display,
                **{k: float(v) if v is not None else None for k, v in student_notes.items()},
            })

        # Calculate ranks after all student data is gathered and then update the DB
        if estudiantes_data and selected_asignacion_id and selected_trimestre_id:
            sorted_estudiantes = sorted(
                [s for s in estudiantes_data if s['prom_trim'] is not None],
                key=lambda x: x['prom_trim'],
                reverse=True
            )

            if sorted_estudiantes:
                current_rank = 1
                for j in range(len(sorted_estudiantes)):
                    if j > 0 and sorted_estudiantes[j]['prom_trim'] != sorted_estudiantes[j-1]['prom_trim']:
                        current_rank = j + 1
                    sorted_estudiantes[j]['rango'] = current_rank

                    estudiante_id = sorted_estudiantes[j]['id']
                    try:
                        resumen_to_update = ResumenTrimestral.objects.get(
                            estudiante_id=estudiante_id,
                            asignacion=selected_asignacion,
                            trimestre=selected_trimestre
                        )
                        resumen_to_update.rango = str(sorted_estudiantes[j]['rango'])
                        resumen_to_update.save()
                    except ResumenTrimestral.DoesNotExist:
                        print(f"Advertencia: ResumenTrimestral no encontrado para estudiante {estudiante_id} al guardar rango.")

                estudiantes_data_map = {s['id']: s for s in estudiantes_data}
                for s in sorted_estudiantes:
                    estudiantes_data_map[s['id']]['rango'] = s['rango']


    context = {
        'selected_asignacion_id': asignacion_id,
        'selected_trimestre_id': trimestre_id,
        'asignaciones': asignaciones,
        'trimestres': trimestres,
        'selected_asignacion': selected_asignacion,
        'selected_trimestre': selected_trimestre,
        'estudiantes_data': estudiantes_data,
        'evaluaciones_saber': evaluaciones_saber,
        'evaluaciones_hacer': evaluaciones_hacer,
    }
    return render(request, 'mi_admin/docente_calificaciones.html', context);


@csrf_exempt
def obtener_conteo_asistencias_ajax(request):
    if request.method == 'GET':
        id_asignacion = request.GET.get('asignacion_id')
        id_trimestre = request.GET.get('trimestre_id')

        if not id_asignacion or not id_trimestre:
            return JsonResponse({'estado': 'error', 'mensaje': 'Los IDs de asignación y trimestre son requeridos.'}, status=400)

        try:
            asignacion_seleccionada = get_object_or_404(Asignacion, id=id_asignacion)
            trimestre_seleccionado = get_object_or_404(Trimestre, id=id_trimestre)

            estudiantes_en_curso = Estudiante.objects.filter(
                curso_actual=asignacion_seleccionada.curso
            ).distinct()

            raw_conteos_asistencia = Asistencia.objects.filter(
                estudiante__in=estudiantes_en_curso,
                asignacion=asignacion_seleccionada,
                trimestre=trimestre_seleccionado,
                asistio=True
            ).values('estudiante_id').annotate(
                conteo=Count('id')
            )

            datos_asistencia_formateados = {
                str(estudiante.id): 0 for estudiante in estudiantes_en_curso
            }
            for item in raw_conteos_asistencia:
                datos_asistencia_formateados[str(item['estudiante_id'])] = item['conteo']

            total_class_days = Asistencia.objects.filter(
                asignacion=asignacion_seleccionada,
                trimestre=trimestre_seleccionado
            ).values('fecha').distinct().count()

            return JsonResponse({
                'estado': 'exito',
                'datos_asistencia': datos_asistencia_formateados,
                'total_class_days': total_class_days
            })
        except Asignacion.DoesNotExist:
            return JsonResponse({'estado': 'error', 'mensaje': 'Asignación no encontrada.'}, status=404)
        except Trimestre.DoesNotExist:
            return JsonResponse({'estado': 'error', 'mensaje': 'Trimestre no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'estado': 'error', 'mensaje': f'Ocurrió un error en el servidor: {str(e)}'}, status=500)
    return JsonResponse({'estado': 'error', 'mensaje': 'Método de solicitud no permitido.'}, status=405)


@require_POST
@csrf_exempt
def guardar_nota_view(request):
    """ Guarda notas individuales para componentes Saber y Hacer. Ya NO recalcula ni guarda 'Ser'. """
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        evaluacion_id = data.get('evaluacion_id')
        valor = data.get('valor')

        if valor is not None and valor != '':
            valor = Decimal(str(valor))
        else:
            valor = None # Permite guardar notas nulas

        estudiante = Estudiante.objects.get(id=estudiante_id)
        evaluacion = Evaluacion.objects.get(id=evaluacion_id)
        asignacion = evaluacion.asignacion
        trimestre = evaluacion.trimestre

        # Actualiza o crea la Nota individual para la evaluación específica
        nota, created = Nota.objects.update_or_create(
            estudiante=estudiante,
            evaluacion=evaluacion,
            defaults={
                'nota_obtenida': valor,
            }
        )

        # Recalcula promedios para Saber y Hacer basados en las notas individuales
        # Sólo considera las evaluaciones de 'Saber' y 'Hacer'
        all_evaluaciones_for_avg = Evaluacion.objects.filter(
            asignacion=asignacion,
            trimestre=trimestre,
            subcomponente__tipo_componente__nombre__in=['Saber', 'Hacer']
        ).select_related('subcomponente__tipo_componente')

        student_notes_query = Nota.objects.filter(
            estudiante=estudiante,
            evaluacion__in=all_evaluaciones_for_avg
        ).select_related('evaluacion__subcomponente__tipo_componente')

        student_notes = {}
        for n in student_notes_query:
            key = f"{n.evaluacion.subcomponente.tipo_componente.nombre.lower()}_eval_{n.evaluacion.id}"
            student_notes[key] = n.nota_obtenida

        evaluaciones_saber = [
            {'id': e.id, 'nombre': e.nombre, 'ponderacion': e.ponderacion, 'note_key': f"{e.subcomponente.tipo_componente.nombre.lower()}_eval_{e.id}"}
            for e in all_evaluaciones_for_avg if e.subcomponente.tipo_componente.nombre.lower() == 'saber'
        ]
        evaluaciones_hacer = [
            {'id': e.id, 'nombre': e.nombre, 'ponderacion': e.ponderacion, 'note_key': f"{e.subcomponente.tipo_componente.nombre.lower()}_eval_{e.id}"}
            for e in all_evaluaciones_for_avg if e.subcomponente.tipo_componente.nombre.lower() == 'hacer'
        ]

        # Calculate weighted average for Saber
        sum_weighted_saber = Decimal(0)
        total_ponderacion_saber = Decimal(0)
        for eval_saber_data in evaluaciones_saber:
            note_key = eval_saber_data['note_key']
            if note_key in student_notes and student_notes[note_key] is not None:
                sum_weighted_saber += student_notes[note_key] * Decimal(str(eval_saber_data['ponderacion']))
                total_ponderacion_saber += Decimal(str(eval_saber_data['ponderacion']))

        prom_saber_calculated = Decimal('0.00')
        if total_ponderacion_saber > 0:
            prom_saber_calculated = (sum_weighted_saber / total_ponderacion_saber).quantize(Decimal('0.01'))


        # Calculate weighted average for Hacer
        sum_weighted_hacer = Decimal(0)
        total_ponderacion_hacer = Decimal(0)
        for eval_hacer_data in evaluaciones_hacer:
            note_key = eval_hacer_data['note_key']
            if note_key in student_notes and student_notes[note_key] is not None:
                sum_weighted_hacer += student_notes[note_key] * Decimal(str(eval_hacer_data['ponderacion']))
                total_ponderacion_hacer += Decimal(str(eval_hacer_data['ponderacion']))

        prom_hacer_calculated = Decimal('0.00')
        if total_ponderacion_hacer > 0:
            prom_hacer_calculated = (sum_weighted_hacer / total_ponderacion_hacer).quantize(Decimal('0.01'))

        # Obtiene el ResumenTrimestral, SIN modificar nota_ser o nota_decidir aquí.
        resumen, created = ResumenTrimestral.objects.get_or_create(
            estudiante=estudiante,
            asignacion=asignacion,
            trimestre=trimestre
        )
        resumen.nota_saber = prom_saber_calculated
        resumen.nota_hacer = prom_hacer_calculated
        # resumen.nota_ser y resumen.nota_decidir NO se actualizan aquí
        resumen.save()


        # Now recalculate the final trimester grade using the utility function
        updated_prom_trim = _recalcular_promedio_final_trimestral(estudiante, asignacion, trimestre)

        return JsonResponse({
            'status': 'success',
            'message': 'Nota guardada exitosamente.',
            'new_prom_saber': float(prom_saber_calculated) if prom_saber_calculated is not None else None,
            'new_prom_hacer': float(prom_hacer_calculated) if prom_hacer_calculated is not None else None,
            'new_prom_trim': float(updated_prom_trim) if updated_prom_trim is not None else None,
            'refresh_data': True # Signal frontend to refresh the main table data
        })

    except Estudiante.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Estudiante no encontrado.'}, status=404)
    except Evaluacion.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Evaluación no encontrada.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido en la solicitud.'}, status=400)
    except Exception as e:
        print(f"Error al guardar nota: {e}")
        return JsonResponse({'status': 'error', 'message': f'Error interno del servidor: {e}'}, status=500)


@csrf_exempt
@require_POST
def crear_subcomponente_evaluacion(request):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponseBadRequest("Solo se permiten solicitudes AJAX.")

    data = request.POST

    action_type = data.get('action_type')

    if action_type == 'create_subcomponente':
        nombre_subcomponente = data.get('nombre_subcomponente')
        tipo_componente_nombre = data.get('tipo_componente_nombre')
        asignacion_id = data.get('asignacion_id')
        trimestre_id = data.get('trimestre_id')
        ponderacion_evaluacion_unica_str = data.get('ponderacion_evaluacion_unica')

        if not all([nombre_subcomponente, tipo_componente_nombre, asignacion_id, trimestre_id, ponderacion_evaluacion_unica_str]):
            return JsonResponse({'status': 'error', 'message': 'Faltan datos para crear el subcomponente y evaluación.'}, status=400)

        try:
            ponderacion_evaluacion_unica = Decimal(ponderacion_evaluacion_unica_str)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Ponderación de evaluación inválida.'}, status=400)

        try:
            asignacion = get_object_or_404(Asignacion, id=asignacion_id)
            trimestre = get_object_or_404(Trimestre, id=trimestre_id)
            tipo_componente = get_object_or_404(TipoComponente, nombre=tipo_componente_nombre)

            # Crea o actualiza el Subcomponente
            subcomponente_obj, subcomponente_created = Subcomponente.objects.get_or_create(
                tipo_componente=tipo_componente,
                nombre=nombre_subcomponente,
                asignacion=asignacion,
                trimestre=trimestre,
                defaults={
                    'porcentaje_maximo': Decimal('100.00'),
                    'ponderacion_evaluacion_unica': ponderacion_evaluacion_unica,
                }
            )

            # Crea o actualiza la Evaluación
            evaluacion_obj, evaluacion_created = Evaluacion.objects.get_or_create(
                asignacion=asignacion,
                trimestre=trimestre,
                subcomponente=subcomponente_obj,
                nombre=nombre_subcomponente,
                defaults={
                    'descripcion': f"Evaluación de {nombre_subcomponente} ({tipo_componente_nombre})",
                    'fecha_evaluacion': date.today(),
                    'ponderacion': ponderacion_evaluacion_unica,
                }
            )
            if not evaluacion_created:
                evaluacion_obj.ponderacion = ponderacion_evaluacion_unica
                evaluacion_obj.save()

            message = "Evaluación creada exitosamente."
            if not subcomponente_created and not evaluacion_created:
                message = "Subcomponente y evaluación ya existían, actualizados."
            elif not subcomponente_created and evaluacion_created:
                message = "Subcomponente existente, nueva evaluación creada."

            return JsonResponse({
                'status': 'success',
                'message': message,
                'evaluacion': {
                    'id': evaluacion_obj.id,
                    'nombre': evaluacion_obj.nombre,
                    'ponderacion': float(evaluacion_obj.ponderacion),
                    'tipo_componente_nombre': tipo_componente_nombre,
                    'note_key': f"{tipo_componente_nombre.lower()}_eval_{evaluacion_obj.id}",
                    'subcomponente_id': subcomponente_obj.id,
                },
                'refresh_data': True
            })

        except Asignacion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Asignación no encontrada.'}, status=404)
        except Trimestre.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Trimestre no encontrado.'}, status=404)
        except TipoComponente.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Tipo de componente no encontrado.'}, status=404)
        except Exception as e:
            print(f"Error al crear subcomponente/evaluación: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Tipo de acción no válido.'}, status=400)


@csrf_exempt
def guardar_observacion(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            estudiante_id = data.get('estudiante_id')
            asignacion_id = data.get('asignacion_id')
            trimestre_id = data.get('trimestre_id')
            observaciones = data.get('observaciones', '')

            if not all([estudiante_id, asignacion_id, trimestre_id]):
                return JsonResponse({'status': 'error', 'message': 'Faltan IDs necesarios para guardar la observación.'}, status=400)

            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                asignacion = Asignacion.objects.get(id=asignacion_id)
                trimestre = Trimestre.objects.get(id=trimestre_id)
            except (Estudiante.DoesNotExist, Asignacion.DoesNotExist, Trimestre.DoesNotExist):
                return JsonResponse({'status': 'error', 'message': 'Entidad (Estudiante, Asignación o Trimestre) no encontrada.'}, status=404)

            resumen, created = ResumenTrimestral.objects.get_or_create(
                estudiante=estudiante,
                asignacion=asignacion,
                trimestre=trimestre
            )

            resumen.observaciones = observaciones
            resumen.save()

            return JsonResponse({'status': 'success', 'message': 'Observación guardada exitosamente.'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error interno del servidor: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Solicitud no válida.'}, status=400)

@csrf_exempt
@require_POST
def guardar_autoevaluacion(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            estudiante_id = data.get('estudiante_id')
            asignacion_id = data.get('asignacion_id')
            trimestre_id = data.get('trimestre_id')
            autoeval_str = data.get('autoeval')

            if not all([estudiante_id, asignacion_id, trimestre_id]):
                return JsonResponse({'status': 'error', 'message': 'Faltan IDs necesarios para guardar la autoevaluación.'}, status=400)

            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                asignacion = Asignacion.objects.get(id=asignacion_id)
                trimestre = Trimestre.objects.get(id=trimestre_id)
            except (Estudiante.DoesNotExist, Asignacion.DoesNotExist, Trimestre.DoesNotExist):
                return JsonResponse({'status': 'error', 'message': 'Entidad (Estudiante, Asignación o Trimestre) no encontrada.'}, status=404)

            autoeval_valor = None
            if autoeval_str is not None and autoeval_str != '':
                try:
                    autoeval_valor = Decimal(autoeval_str)
                    if not (0 <= autoeval_valor <= 10):
                        return JsonResponse({'status': 'error', 'message': 'El valor de autoevaluación debe estar entre 0 y 10.'}, status=400)
                except InvalidOperation:
                    return JsonResponse({'status': 'error', 'message': 'Valor de autoevaluación inválido.'}, status=400)

            resumen, created = ResumenTrimestral.objects.get_or_create(
                estudiante=estudiante,
                asignacion=asignacion,
                trimestre=trimestre
            )

            resumen.autoeval = autoeval_valor
            resumen.save()

            updated_prom_trim = _recalcular_promedio_final_trimestral(estudiante, asignacion, trimestre)

            return JsonResponse({
                'status': 'success',
                'message': 'Autoevaluación guardada exitosamente.',
                'new_prom_trim': float(updated_prom_trim) if updated_prom_trim is not None else None,
                'refresh_data': True
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error interno del servidor: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Solicitud no válida.'}, status=400)


@csrf_exempt
@require_POST
def guardar_nota_decidir(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            estudiante_id = data.get('estudiante_id')
            asignacion_id = data.get('asignacion_id')
            trimestre_id = data.get('trimestre_id')
            valor_str = data.get('valor')

            if not all([estudiante_id, asignacion_id, trimestre_id]):
                return JsonResponse({'status': 'error', 'message': 'Faltan IDs necesarios.'}, status=400)

            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                asignacion = Asignacion.objects.get(id=asignacion_id)
                trimestre = Trimestre.objects.get(id=trimestre_id)
            except (Estudiante.DoesNotExist, Asignacion.DoesNotExist, Trimestre.DoesNotExist):
                return JsonResponse({'status': 'error', 'message': 'Entidad no encontrada.'}, status=404)

            valor = None
            if valor_str is not None and valor_str != '':
                try:
                    valor = Decimal(valor_str)
                    if not (0 <= valor <= 10):
                        return JsonResponse({'status': 'error', 'message': 'El valor de Decidir debe estar entre 0 y 10.'}, status=400)
                except InvalidOperation:
                    return JsonResponse({'status': 'error', 'message': 'Valor de nota inválido.'}, status=400)

            resumen, created = ResumenTrimestral.objects.get_or_create(
                estudiante=estudiante,
                asignacion=asignacion,
                trimestre=trimestre
            )

            resumen.nota_decidir = valor
            resumen.save()

            updated_prom_trim = _recalcular_promedio_final_trimestral(estudiante, asignacion, trimestre)

            return JsonResponse({
                'status': 'success',
                'message': 'Nota de Decidir guardada exitosamente.',
                'new_prom_trim': float(updated_prom_trim) if updated_prom_trim is not None else None,
                'refresh_data': True
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Solicitud no válida.'}, status=400)


@csrf_exempt
@require_POST
def guardar_nota_ser(request):
    """
    Guarda directamente la nota para el componente 'Ser' en el ResumenTrimestral.
    Funciona de forma similar a guardar_nota_decidir o guardar_autoevaluacion.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            estudiante_id = data.get('estudiante_id')
            asignacion_id = data.get('asignacion_id')
            trimestre_id = data.get('trimestre_id')
            valor_str = data.get('valor')

            if not all([estudiante_id, asignacion_id, trimestre_id]):
                return JsonResponse({'status': 'error', 'message': 'Faltan IDs necesarios.'}, status=400)

            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                asignacion = Asignacion.objects.get(id=asignacion_id)
                trimestre = Trimestre.objects.get(id=trimestre_id)
            except (Estudiante.DoesNotExist, Asignacion.DoesNotExist, Trimestre.DoesNotExist):
                return JsonResponse({'status': 'error', 'message': 'Entidad no encontrada.'}, status=404)

            valor = None
            if valor_str is not None and valor_str != '':
                try:
                    valor = Decimal(valor_str)
                    # Assuming 'Ser' is graded on a 0-10 scale, consistent with Decidir and Autoevaluacion
                    if not (0 <= valor <= 10):
                        return JsonResponse({'status': 'error', 'message': 'El valor de Ser debe estar entre 0 y 10.'}, status=400)
                except InvalidOperation:
                    return JsonResponse({'status': 'error', 'message': 'Valor de nota inválido.'}, status=400)

            resumen, created = ResumenTrimestral.objects.get_or_create(
                estudiante=estudiante,
                asignacion=asignacion,
                trimestre=trimestre
            )

            resumen.nota_ser = valor # Asigna directamente el valor a nota_ser
            resumen.save()

            # Recalcula el promedio final trimestral para reflejar el cambio en 'Ser'
            updated_prom_trim = _recalcular_promedio_final_trimestral(estudiante, asignacion, trimestre)

            return JsonResponse({
                'status': 'success',
                'message': 'Nota de Ser guardada exitosamente.',
                'new_prom_trim': float(updated_prom_trim) if updated_prom_trim is not None else None,
                'new_prom_ser': float(valor) if valor is not None else None, # Retorna el valor guardado de Ser
                'refresh_data': True # Indicar al frontend que recargue o actualice datos
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Solicitud no válida.'}, status=400)

@require_http_methods(["PATCH", "DELETE"])
def editar_o_eliminar_evaluacion_subcomponente(request, evaluacion_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'No autenticado'}, status=401)
    
    # Opcional: Verificar si el usuario es un docente y tiene permisos para esta asignación/trimestre
    # Esto requeriría pasar asignacion_id y trimestre_id o buscarlo a través de la evaluación_id.
    # Por simplicidad, omitiremos la lógica detallada de permisos aquí, pero es crucial en un entorno real.

    try:
        # Recuperar la Evaluación. Si se elimina, queremos el ID de la Evaluación.
        # Si se edita, el ID de la Evaluación nos permite encontrar el Subcomponente asociado.
        evaluacion = Evaluacion.objects.get(id=evaluacion_id)
        subcomponente = evaluacion.subcomponente # Accede al Subcomponente relacionado
    except Evaluacion.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Evaluación no encontrada'}, status=404)
    except Subcomponente.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Subcomponente asociado no encontrado'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            action_type = data.get('action_type')

            if action_type == 'edit_subcomponente':
                nuevo_nombre = data.get('nombre')
                nueva_ponderacion_evaluacion = data.get('ponderacion_evaluacion') # Este es para la EVALUACION

                if not nuevo_nombre:
                    return JsonResponse({'status': 'error', 'message': 'El nombre del subcomponente no puede estar vacío.'}, status=400)
                if nueva_ponderacion_evaluacion is None or not isinstance(nueva_ponderacion_evaluacion, (int, float)) or nueva_ponderacion_evaluacion < 0:
                    return JsonResponse({'status': 'error', 'message': 'La ponderación debe ser un número positivo.'}, status=400)

                # Actualiza la Evaluación específica (su nombre y ponderación)
                evaluacion.nombre = nuevo_nombre
                evaluacion.ponderacion = nueva_ponderacion_evaluacion
                evaluacion.save()

                # Opcional: Si quieres actualizar también la `ponderacion_evaluacion_unica` del Subcomponente padre,
                # podrías hacerlo aquí, pero la interfaz solo sugiere editar la evaluación individual.
                # subcomponente.ponderacion_evaluacion_unica = nueva_ponderacion_evaluacion
                # subcomponente.save()

                return JsonResponse({'status': 'success', 'message': 'Evaluación actualizada exitosamente.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Tipo de acción PATCH no reconocido.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error interno al actualizar: {str(e)}'}, status=500)

    elif request.method == 'DELETE':
        try:
            # Eliminar la Evaluación
            evaluacion.delete()
            return JsonResponse({'status': 'success', 'message': 'Evaluación eliminada exitosamente.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error interno al eliminar: {str(e)}'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

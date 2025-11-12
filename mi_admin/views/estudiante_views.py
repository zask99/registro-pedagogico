# mi_admin/views/estudiante_views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, ObjectDoesNotExist
from django.utils import timezone

# Importa los modelos necesarios
from mi_admin.models import Usuario, Persona, Estudiante, Curso, Inscripcion, Asignacion, Trimestre, Evaluacion, Nota, ResumenTrimestral, Asistencia, TipoComponente, Subcomponente, Docente

# Decorador para asegurar que solo usuarios autenticados y con rol de Estudiante puedan acceder
def estudiante_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            user = request.user
            # Asegúrate de que el usuario tiene un rol asignado antes de intentar acceder a 'nombre'
            if not user.rol:
                raise Http404("Acceso denegado. Tu cuenta no tiene un rol asignado.")

            # Verifica si el rol del usuario no es 'Estudiante'
            if user.rol.nombre != 'Estudiante':
                raise Http404("Acceso denegado. Tu rol no es de Estudiante.")
            
            # Obtener el perfil de Persona asociado al Usuario
            persona = Persona.objects.get(usuario=user)
            # Obtener el perfil de Estudiante asociado a esa Persona
            estudiante = persona.estudiante_perfil # Esto accede al related_name 'estudiante_perfil'

            request.estudiante_perfil = estudiante
            return view_func(request, *args, **kwargs)
        except (Persona.DoesNotExist, Estudiante.DoesNotExist):
            raise Http404("Perfil de estudiante no encontrado o no asociado a tu cuenta.")
        except ObjectDoesNotExist: # Captura si el rol no existe o es nulo inesperadamente
            raise Http404("Perfil de estudiante o rol no encontrado.")
        except Exception as e:
            print(f"Error en estudiante_required: {e}")
            raise Http404(f"Ocurrió un error al verificar tu perfil. Acceso denegado. Detalles: {e}")
    return _wrapped_view

# Dashboard del estudiante (ejemplo, ajusta si tu dashboard está en otra vista)
@estudiante_required
def dashboard_estudiante(request):
    user = request.user
    estudiante = request.estudiante_perfil
    
    # Aquí puedes añadir la lógica necesaria para el dashboard,
    # como obtener el curso actual, últimas calificaciones, etc.
    # Por ahora, solo pasa los objetos básicos.
    
    context = {
        'user': user,
        'estudiante': estudiante,
        # Puedes añadir más datos aquí para tu dashboard si es necesario
    }
    return render(request, 'mi_admin/dashboard_estudiante.html', context)


@estudiante_required
def ver_mis_calificaciones(request):
    user = request.user
    estudiante = request.estudiante_perfil

    current_year = timezone.now().year
    materias_con_notas = {}

    try:
        # Optimizado con select_related para traer todos los objetos relacionados de una vez
        resumenes_trimestrales = ResumenTrimestral.objects.filter(
            estudiante=estudiante,
            asignacion__anio_academico=current_year
        ).select_related(
            'asignacion__materia', 
            'asignacion__curso', 
            'asignacion__docente__persona', # Añadido para acceder al docente si es necesario
            'trimestre'
        ).order_by(
            'asignacion__curso__grado', 
            'asignacion__curso__paralelo', 
            'asignacion__materia__nombre',
            'trimestre__gestion', 
            'trimestre__numero'
        )

        for resumen in resumenes_trimestrales:
            try:
                materia_nombre = resumen.asignacion.materia.nombre
                curso_obj = resumen.asignacion.curso
                curso_nombre = f"{curso_obj.grado} '{curso_obj.paralelo}' - {curso_obj.get_niveles_display()}"
                
                # Acceso al nombre completo del docente
                docente_nombre = None
                if resumen.asignacion.docente and resumen.asignacion.docente.persona:
                    docente_nombre = resumen.asignacion.docente.persona.get_full_name()

                if materia_nombre not in materias_con_notas:
                    materias_con_notas[materia_nombre] = {
                        'curso': curso_nombre,
                        'docente': docente_nombre, # Añadido el nombre del docente
                        'trimestres': {}
                    }
                trimestre_key = f"{resumen.trimestre.nombre} ({resumen.trimestre.gestion})"
                materias_con_notas[materia_nombre]['trimestres'][trimestre_key] = {
                    'nota_final': resumen.nota_final_trimestre,
                    'saber': resumen.nota_saber,
                    'hacer': resumen.nota_hacer,
                    'decidir': resumen.nota_decidir,
                    'ser': resumen.nota_ser,
                    'observaciones': resumen.observaciones, # CORREGIDO: Usar 'observaciones'
                    'resumen_id': resumen.id,
                }
            except ObjectDoesNotExist as e:
                print(f"Error al procesar resumen (objeto relacionado no existe): {e} para Resumen ID: {resumen.id}")
            except AttributeError as e:
                print(f"Error de atributo al procesar resumen: {e} para Resumen ID: {resumen.id}")
            except Exception as e:
                print(f"Error inesperado al procesar resumen: {e} para Resumen ID: {resumen.id}")

    except Exception as e:
        print(f"Error al obtener o procesar resumenes_trimestrales: {e}")

    context = {
        'user': user,
        'estudiante': estudiante,
        'materias_con_notas': materias_con_notas,
        'current_year': current_year,
    }
    return render(request, 'mi_admin/est_mis_calificaciones.html', context)


@estudiante_required
def ver_detalle_calificacion(request, resumen_id):
    user = request.user
    estudiante = request.estudiante_perfil
    resumen = None
    notas_detalladas = Nota.objects.none()

    try:
        resumen = get_object_or_404(
            ResumenTrimestral.objects.select_related(
                'asignacion__materia', 
                'asignacion__curso', 
                'trimestre', 
                'asignacion__docente__persona' # Para acceder a los datos del docente
            ),
            id=resumen_id,
            estudiante=estudiante
        )

        notas_detalladas = Nota.objects.filter(
            estudiante=estudiante,
            evaluacion__asignacion=resumen.asignacion,
            evaluacion__trimestre=resumen.trimestre
        ).select_related('evaluacion__subcomponente__tipo_componente').order_by(
            'evaluacion__subcomponente__tipo_componente__nombre', 
            'evaluacion__fecha_evaluacion',
            'evaluacion__nombre' # Añadido para un orden más consistente
        )

    except Http404:
        raise
    except Exception as e:
        print(f"Error en ver_detalle_calificacion para resumen_id {resumen_id}: {e}")
        raise Http404("Ocurrió un error al cargar el detalle de la calificación.")

    context = {
        'user': user,
        'estudiante': estudiante,
        'resumen': resumen,
        'notas_detalladas': notas_detalladas,
    }
    return render(request, 'mi_admin/est_detalle_calificacion.html', context)


@estudiante_required
def listar_mis_cursos_estudiante(request):
    user = request.user
    estudiante = request.estudiante_perfil

    current_year = timezone.now().year
    inscripciones = Inscripcion.objects.none()
    curso_actual = None

    try:
        inscripciones = Inscripcion.objects.filter(
            estudiante=estudiante,
            anio_academico=current_year
        ).select_related('curso').order_by('curso__grado', 'curso__paralelo')

        curso_actual = estudiante.curso_actual

    except Exception as e:
        print(f"Error al obtener inscripciones o curso actual: {e}")

    # --- DEBUGGING: Imprime los datos para verificar si la consulta trae resultados. ---
    print(f"\n--- DEBUGGING DE LISTAR_MIS_CURSOS_ESTUDIANTE ---")
    print(f"Usuario autenticado: {user.username}")
    if estudiante and estudiante.persona: # Asegurarse de que persona existe
        print(f"Estudiante ID: {estudiante.id}, Nombres: {estudiante.persona.nombres} {estudiante.persona.apellidos}")
    else:
        print(f"Estudiante o Persona no disponible para debugging.")
    print(f"Año Actual (current_year): {current_year}")

    if inscripciones.exists():
        print(f"Inscripciones encontradas para el año {current_year}: {inscripciones.count()}")
        for inscripcion in inscripciones:
            try:
                print(f"   - Inscrito en Curso: {inscripcion.curso.grado} '{inscripcion.curso.paralelo}' - {inscripcion.curso.get_niveles_display()}")
                print(f"     Fecha Inscripción: {inscripcion.fecha_inscripcion}, Año Académico: {inscripcion.anio_academico}")
            except ObjectDoesNotExist:
                print(f"   - Inscripción {inscripcion.id}: Curso relacionado no encontrado.")
            except AttributeError as e:
                print(f"   - Inscripción {inscripcion.id}: Error de atributo al acceder al curso: {e}")
            except Exception as e:
                print(f"   - Inscripción {inscripcion.id}: Error inesperado al procesar: {e}")
    else:
        print(f"NO se encontraron inscripciones para el estudiante {estudiante.persona.nombres if estudiante and estudiante.persona else 'N/A'} para el año {current_year}.")

    if curso_actual:
        try:
            print(f"Curso actual del estudiante (desde Estudiante.curso_actual): {curso_actual.grado} '{curso_actual.paralelo}' - {curso_actual.get_niveles_display()}")
        except AttributeError as e:
            print(f"Error de atributo al acceder a curso_actual: {e}")
        except Exception as e:
            print(f"Error inesperado al acceder a curso_actual: {e}")
    else:
        print("El estudiante NO tiene un 'curso_actual' asignado en su perfil.")
    print(f"--- FIN DEBUGGING ---\n")

    context = {
        'user': user,
        'estudiante': estudiante,
        'inscripciones': inscripciones,
        'curso_actual': curso_actual,
        'current_year': current_year,
    }
    # La plantilla para mis cursos se llama 'est_mis_cursos.html' y está en 'mi_admin/'
    return render(request, 'mi_admin/est_mis_cursos.html', context)


@estudiante_required
def ver_mi_asistencia(request):
    user = request.user
    estudiante = request.estudiante_perfil

    current_year = timezone.now().year
    asistencias = Asistencia.objects.none()
    total_clases = 0
    presentes = 0
    ausentes = 0
    porcentaje_asistencia = "0.00"

    try:
        asistencias = Asistencia.objects.filter(
            estudiante=estudiante,
            asignacion__anio_academico=current_year
        ).select_related('asignacion__materia', 'asignacion__curso', 'trimestre').order_by(
            '-fecha', 'asignacion__materia__nombre'
        )

        total_clases = asistencias.count()
        presentes = asistencias.filter(asistio=True).count()
        ausentes = total_clases - presentes
        porcentaje_asistencia = (Decimal(str(presentes)) / Decimal(str(total_clases)) * 100) if total_clases > 0 else Decimal('0.00')
        porcentaje_asistencia = f"{porcentaje_asistencia:.2f}"

    except Exception as e:
        print(f"Error al obtener o calcular asistencia: {e}")

    context = {
        'user': user,
        'estudiante': estudiante,
        'asistencias': asistencias,
        'total_clases': total_clases,
        'presentes': presentes,
        'ausentes': ausentes,
        'porcentaje_asistencia': porcentaje_asistencia,
        'current_year': current_year,
    }
    return render(request, 'mi_admin/est_mis_asistencias.html', context)
# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\views\administrativo_views.py
print(">>> ADMINISTRATIVO_VIEWS.PY HA SIDO CARGADO EN ESTA EJECUCIÓN <<<")
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test

# --- INICIO DE MODIFICACIÓN ---
# Importar los modelos y logging necesarios
from mi_admin.models import Curso, Estudiante, Materia, Trimestre, Administrativo 
import logging
logger = logging.getLogger(__name__)
# --- FIN DE MODIFICACIÓN ---

from mi_admin.forms import PersonaForm, EstudianteForm, DocenteForm, AdministrativoForm


def is_administrativo(user):
    return user.is_authenticated and hasattr(user, 'rol') and user.rol.nombre == 'Administrativo'


# --- INICIO DE MODIFICACIÓN ---
# Reemplazada la vista del dashboard por la versión que busca el nombre
@login_required
@user_passes_test(is_administrativo, login_url='/')
def dashboard_administrativo(request):
    """
    Vista principal (Dashboard) para el Administrador.
    Muestra la bienvenida con el nombre completo.
    """
    logger.debug(f"[{request.user.username}] Accediendo a dashboard_administrativo_view")
    try:
        # 1. Obtener el perfil Administrativo basado en el usuario logueado
        admin_user = get_object_or_404(Administrativo.objects.select_related('persona'), persona__usuario=request.user)
        
        # 2. Obtener el nombre completo desde el modelo Persona
        nombre_completo_admin = admin_user.persona.get_full_name()

        # 3. Preparar el contexto
        context = {
            # Pasamos el nombre completo a la plantilla
            'nombre_admin': nombre_completo_admin, 
        }
        
        # 4. Renderizar la plantilla
        return render(request, 'mi_admin/dashboard_administrativo.html', context)
    
    except Administrativo.DoesNotExist:
        logger.error(f"[{request.user.username}] (Dashboard Admin) No se encontró el perfil de admin asociado.")
        messages.error(request, "Acceso denegado. No tiene un perfil de admin asociado.")
        return redirect('logout')
    except Exception as e:
        logger.exception(f"[{request.user.username}] (Dashboard Admin) Ocurrió un error: {e}")
        messages.error(request, f"Ocurrió un error inesperado: {e}")
        return render(request, 'mi_admin/dashboard_administrativo.html', {})
# --- FIN DE MODIFICACIÓN ---


@login_required
@user_passes_test(is_administrativo, login_url='/')
def listar_cursos_admin(request):
    cursos = Curso.objects.all().order_by('nombre')
    return render(request, 'mi_admin/listar_cursos_admin.html', {'cursos': cursos})


@login_required
@user_passes_test(is_administrativo, login_url='/')
def listar_estudiantes_por_curso_admin(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    estudiantes = Estudiante.objects.filter(curso_actual=curso).order_by('persona__apellidos', 'persona__nombres')
    return render(request, 'mi_admin/listar_estudiantes_por_curso_admin.html', {'curso': curso, 'estudiantes': estudiantes})


@login_required
@user_passes_test(is_administrativo, login_url='/')
@transaction.atomic
def registrar_persona(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        persona_form = PersonaForm(request.POST)

        if persona_form.is_valid():
            try:
                persona = persona_form.save()

                if tipo == 'estudiante':
                    estudiante_form = EstudianteForm(request.POST)
                    if estudiante_form.is_valid():
                        estudiante = estudiante_form.save(commit=False)
                        estudiante.persona = persona
                        estudiante.save()
                        messages.success(request, 'Estudiante registrado exitosamente.')
                        return redirect('registrar_persona')
                    else:
                        messages.error(request, "Error en datos del Estudiante.")

                elif tipo == 'docente':
                    docente_form = DocenteForm(request.POST)
                    if docente_form.is_valid():
                        docente = docente_form.save(commit=False)
                        docente.persona = persona
                        docente.save()
                        docente_form.save_m2m()
                        messages.success(request, 'Docente registrado exitosamente.')
                        return redirect('registrar_persona')
                    else:
                        messages.error(request, "Error en datos del Docente.")

                elif tipo == 'administrativo':
                    administrativo_form = AdministrativoForm(request.POST)
                    if administrativo_form.is_valid():
                        administrativo = administrativo_form.save(commit=False)
                        administrativo.persona = persona
                        administrativo.save()
                        messages.success(request, 'Administrativo registrado exitosamente.')
                        return redirect('registrar_persona')
                    else:
                        messages.error(request, "Error en datos del Administrativo.")

                else:
                    messages.error(request, 'Tipo inválido.')

            except Exception as e:
                messages.error(request, f"Error inesperado: {e}")
        else:
            messages.error(request, "Error en datos personales.")
    else:
        persona_form = PersonaForm()
        estudiante_form = EstudianteForm()
        docente_form = DocenteForm()
        administrativo_form = AdministrativoForm()

    context = {
        'persona_form': persona_form,
        'estudiante_form': estudiante_form,
        'docente_form': docente_form,
        'administrativo_form': administrativo_form,
        'cursos': Curso.objects.all().order_by('nombre'),
        'materias': Materia.objects.all().order_by('nombre'),
    }
    return render(request, 'mi_admin/registro_persona.html', context)

@login_required
@user_passes_test(is_administrativo, login_url='/')
def admin_listar_trimestres(request):
    print("--- DEBUG: INICIO de la vista admin_listar_trimestres ---") # MENSAJE CLAVE 1

    # ESTE ES EL BLOQUE QUE ESTABA DENTRO DEL TRY, AHORA ESTÁ SIN ÉL
    # Si hay un error aquí, Django mostrará una traceback completa en la consola.
    trimestres = Trimestre.objects.all().order_by('gestion', 'numero')
    print(f"--- DEBUG: Se obtuvieron {trimestres.count()} trimestres de la base de datos. ---") # MENSAJE CLAVE 2

    context = {
        'trimestres': trimestres,
    }

    print("--- DEBUG: Intentando renderizar admin_listar_trimestres.html ---") # MENSAJE CLAVE 3
    return render(request, 'mi_admin/admin_listar_trimestres.html', context)
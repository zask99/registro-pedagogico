# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\views\admin_registrar_persona_views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction, IntegrityError
from django.utils import timezone
from django.contrib.auth.hashers import make_password # <-- NUEVA IMPORTACIÓN
import pandas as pd # <-- NUEVA IMPORTACIÓN

# Asegúrate de que los formularios y modelos estén importados correctamente
from mi_admin.forms import UsuarioForm, PersonaForm, EstudianteForm, DocenteForm, AdministrativoForm
from mi_admin.models import Usuario, Rol, Estudiante, Docente, Administrativo, Persona, Inscripcion, Curso 

# Función auxiliar para verificar si el usuario es administrador
def is_administrador(user):
    return user.is_authenticated and hasattr(user, 'rol') and user.rol and user.rol.nombre.lower().strip() == 'administrativo'

# --- MODIFICADO ---
# Función auxiliar para renderizar el request con los formularios correctos
def render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form):
    context = {
        'usuario_form': usuario_form,
        'persona_form': persona_form,
        'estudiante_form': estudiante_form,
        'docente_form': docente_form,
        'administrativo_form': administrativo_form,
        'cursos': Curso.objects.all().order_by('niveles', 'grado', 'paralelo') # <-- AÑADIDO: Pasa los cursos
    }
    return render(request, 'mi_admin/registrar_persona.html', context)


@login_required
@user_passes_test(is_administrador, login_url='/login/')
@transaction.atomic 
def registrar_persona(request):
    
    # --- MODIFICADO: Lógica GET ahora usa la función auxiliar ---
    if request.method != 'POST':
        usuario_form = UsuarioForm(prefix='usuario')
        persona_form = PersonaForm(prefix='persona')
        estudiante_form = EstudianteForm(prefix='estudiante')
        docente_form = DocenteForm(prefix='docente')
        administrativo_form = AdministrativoForm(prefix='administrativo')
        return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)

    # --- LÓGICA POST (Sin cambios) ---
    
    usuario_form = UsuarioForm(request.POST, prefix='usuario')
    persona_form = PersonaForm(request.POST, prefix='persona')
    estudiante_form = EstudianteForm(request.POST, prefix='estudiante')
    docente_form = DocenteForm(request.POST, prefix='docente')
    administrativo_form = AdministrativoForm(request.POST, prefix='administrativo')

    if not (usuario_form.is_valid() and persona_form.is_valid()):
        messages.error(request, 'Por favor, corrija los errores en "Datos de Cuenta" o "Datos Personales".')
        return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)

    selected_rol = usuario_form.cleaned_data.get('rol')
    selected_rol_name = selected_rol.nombre.lower().strip()
    persona_data = persona_form.cleaned_data
    
    generated_username = ""
    generated_password = ""
    email = request.POST.get('usuario-email', '').strip() 

    if not email:
        messages.error(request, "El campo Email es obligatorio para todos los roles.")
        return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)

    profile_form_valid = False

    if selected_rol_name == 'estudiante':
        if estudiante_form.is_valid():
            generated_username = estudiante_form.cleaned_data.get('codigo_estudiante', '').strip()
            generated_password = persona_data.get('carnet', '').strip()
            if not generated_username or not generated_password:
                messages.error(request, "Para Estudiantes, el Código RUDE y el Carnet son obligatorios.")
                return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)
            profile_form_valid = True
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario de Estudiante.')

    elif selected_rol_name == 'docente':
        if docente_form.is_valid():
            generated_username = request.POST.get('usuario-username', '').strip()
            generated_password = request.POST.get('usuario-password', '').strip()
            if not generated_username or not generated_password:
                messages.error(request, "Para Docentes, el Nombre de Usuario y la Contraseña son obligatorios.")
                return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)
            profile_form_valid = True
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario de Docente.')

    elif selected_rol_name == 'administrativo':
        if administrativo_form.is_valid():
            generated_username = request.POST.get('usuario-username', '').strip()
            generated_password = request.POST.get('usuario-password', '').strip()
            if not generated_username or not generated_password:
                messages.error(request, "Para Administrativos, el Nombre de Usuario y la Contraseña son obligatorios.")
                return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)
            profile_form_valid = True
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario de Administrativo.')
    else:
        messages.error(request, 'Rol seleccionado no válido o no manejado.')

    if not profile_form_valid:
        return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)

    try:
        if Usuario.objects.filter(username=generated_username).exists():
            messages.error(request, f"Ya existe un usuario con el nombre de usuario '{generated_username}'.")
            return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)
        
        user = Usuario(
            username=generated_username,
            email=email,
            rol=selected_rol,
            is_active=True,
            first_name=persona_data.get('nombres'),
            last_name=persona_data.get('apellidos')
        )
        user.set_password(generated_password) 
        user.save()

        persona = Persona.objects.create(
            usuario=user,
            nombres=persona_data.get('nombres'),
            apellidos=persona_data.get('apellidos'),
            carnet=persona_data.get('carnet'),
            fecha_nacimiento=persona_data.get('fecha_nacimiento'),
            genero=persona_data.get('genero'),
            pais=persona_data.get('pais'),
            departamento=persona_data.get('departamento'),
            provincia=persona_data.get('provincia'),
            localidad=persona_data.get('localidad')
        )

        if selected_rol_name == 'estudiante':
            estudiante = estudiante_form.save(commit=False)
            estudiante.persona = persona 
            estudiante.save()
            curso_seleccionado = estudiante_form.cleaned_data.get('curso_actual')
            if curso_seleccionado:
                current_year = timezone.now().year
                Inscripcion.objects.create(
                    estudiante=estudiante,
                    curso=curso_seleccionado,
                    anio_academico=current_year
                )
                messages.success(request, f'Estudiante registrado e inscrito en {curso_seleccionado.get_full_name()}. Usuario: {generated_username}, Contraseña: {generated_password}')
            else:
                messages.warning(request, f"Estudiante registrado (sin curso). Usuario: {generated_username}, Contraseña: {generated_password}")

        elif selected_rol_name == 'docente':
            docente = docente_form.save(commit=False)
            docente.persona = persona 
            docente.save()
            messages.success(request, f'Docente registrado. Usuario: {generated_username}, Contraseña: {generated_password}')

        elif selected_rol_name == 'administrativo':
            administrativo = administrativo_form.save(commit=False)
            administrativo.persona = persona 
            administrativo.save()
            messages.success(request, f'Administrativo registrado. Usuario: {generated_username}, Contraseña: {generated_password}')

        return redirect('mi_admin:dashboard_administrativo') 

    except IntegrityError as e:
        messages.error(request, f"Error de Integridad: {e}. Es posible que el Carnet ya esté en uso.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error inesperado al guardar en la base de datos: {e}")

    return render_request_with_forms(request, usuario_form, persona_form, estudiante_form, docente_form, administrativo_form)

# --- INICIO DE LA NUEVA VISTA DE IMPORTACIÓN (CORREGIDA) ---
@login_required
@user_passes_test(is_administrador, login_url='/login/')
def importar_estudiantes_excel(request):
    if request.method != 'POST':
        messages.error(request, "Método no permitido.")
        return redirect('mi_admin:registrar_persona')

    try:
        excel_file = request.FILES.get('excel_file')
        curso_id = request.POST.get('curso_id')

        if not excel_file or not curso_id:
            messages.error(request, "Debe seleccionar un curso Y un archivo para importar.")
            return redirect('mi_admin:registrar_persona')

        # Obtener los objetos fijos
        curso_obj = Curso.objects.get(pk=curso_id)
        rol_estudiante = Rol.objects.get(nombre__iexact='estudiante') # Búscalo por nombre
        current_year = timezone.now().year

        # Detectar tipo de archivo y leerlo correctamente
        file_name = excel_file.name
        df = None

        if file_name.endswith('.csv'):
            df = pd.read_csv(excel_file, dtype=str)
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(excel_file, dtype=str, engine='openpyxl')
        else:
            messages.error(request, "Formato de archivo no válido. Use .xlsx o .csv")
            return redirect('mi_admin:registrar_persona')

        df = df.where(pd.notnull(df), None) # Reemplazar NaN por None

        exitosos = 0
        errores = []

        with transaction.atomic(): 
            for index, fila in df.iterrows():
                try:
                    # Convertir a str() antes de .strip()
                    rude = str(fila.get('codigo_rude', '') or '').strip()
                    carnet = str(fila.get('carnet', '') or '').strip()
                    nombres = str(fila.get('nombres', '') or '').strip()
                    apellidos = str(fila.get('apellidos', '') or '').strip()
                    email = str(fila.get('email', '') or '').strip()
                    
                    if not (rude and carnet and nombres and apellidos and email):
                        raise ValueError("Faltan datos obligatorios (RUDE, Carnet, Nombres, Apellidos o Email).")

                    if Usuario.objects.filter(username=rude).exists():
                        raise IntegrityError(f"El usuario (RUDE) '{rude}' ya existe.")
                    if Persona.objects.filter(carnet=carnet).exists():
                         raise IntegrityError(f"El Carnet '{carnet}' ya está registrado.")

                    user = Usuario(
                        username=rude,
                        email=email,
                        rol=rol_estudiante,
                        is_active=True,
                        first_name=nombres,
                        last_name=apellidos
                    )
                    user.set_password(carnet) 
                    user.save()

                    # 5. Crear Persona
                    fecha_nac_str = fila.get('fecha_nacimiento')
                    genero_str = fila.get('genero')
                    
                    # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
                    # Limpiamos la fecha que Pandas ensucia.
                    fecha_nac_limpia = None
                    if fecha_nac_str:
                        # Convertimos a string (por si acaso) y cortamos la parte de la hora
                        fecha_nac_limpia = str(fecha_nac_str).split(' ')[0]
                    # --- FIN DE LA CORRECCIÓN ---

                    persona = Persona.objects.create(
                        usuario=user,
                        nombres=nombres,
                        apellidos=apellidos,
                        carnet=carnet,
                        # Usamos la fecha limpia
                        fecha_nacimiento=fecha_nac_limpia if fecha_nac_limpia else None,
                        genero=genero_str if genero_str else None,
                        pais=fila.get('pais') if fila.get('pais') else 'Bolivia',
                        departamento=fila.get('departamento'),
                        provincia=fila.get('provincia'),
                        localidad=fila.get('localidad')
                    )

                    # 6. Crear Estudiante
                    estudiante = Estudiante.objects.create(
                        persona=persona,
                        codigo_estudiante=rude,
                        curso_actual=curso_obj
                    )
                    
                    # 7. Crear Inscripción
                    Inscripcion.objects.create(
                        estudiante=estudiante,
                        curso=curso_obj,
                        anio_academico=current_year
                    )
                    
                    exitosos += 1

                except (ValueError, IntegrityError) as e:
                    errores.append(f"Fila {index + 2}: {e}")
                    break 
                except Exception as e:
                    errores.append(f"Fila {index + 2}: Error inesperado - {e}")
                    break 

            if errores:
                raise Exception("Se encontraron errores. Revirtiendo todos los cambios.")

        messages.success(request, f"¡Éxito! Se importaron {exitosos} estudiantes al curso '{curso_obj.get_full_name()}'")

    except Exception as e:
        messages.error(request, f"Falló la importación masiva. Error: {e}")
        if 'errores' in locals() and errores:
            error_list = "\\n".join(errores[:5])
            if len(errores) > 5:
                error_list += f"\\n... y {len(errores) - 5} errores más."
            messages.warning(request, f"Detalles de errores: \\n{error_list}")

    return redirect('mi_admin:registrar_persona')
# --- FIN DE LA NUEVA VISTA DE IMPORTACIÓN ---
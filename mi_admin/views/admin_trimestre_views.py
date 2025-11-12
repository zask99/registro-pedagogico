# mi_admin/views/admin_trimestre_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from mi_admin.models import Trimestre
from mi_admin.forms import TrimestreForm
from mi_admin.permissions import is_administrativo

@login_required
@user_passes_test(is_administrativo, login_url='/')
def admin_listar_trimestres(request):
    print("--- DEBUG (admin_trimestre_views): INICIO de la vista admin_listar_trimestres ---")

    trimestres = Trimestre.objects.all().order_by('-gestion', 'fecha_inicio')
    print(f"--- DEBUG (admin_trimestre_views): Se obtuvieron {trimestres.count()} trimestres de la BD. ---")

    # --- ¡ESTE ES EL BLOQUE QUE NECESITAS RE-AGREGAR O DESCOMENTAR! ---
    if request.method == 'POST':
        form = TrimestreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trimestre creado exitosamente.")
            print("--- DEBUG (admin_trimestre_views): Formulario de trimestre válido, guardado y redirigiendo. ---") # Mensaje de depuración
            return redirect('mi_admin:admin_listar_trimestres') # Redirige al mismo listado para ver el nuevo trimestre
        else:
            # Si el formulario no es válido, se volverá a renderizar con los errores
            messages.error(request, "Error al crear el trimestre. Por favor, revise los datos.")
            print(f"--- DEBUG (admin_trimestre_views): Formulario de trimestre NO válido. Errores: {form.errors} ---") # Mensaje de depuración
    else:
        form = TrimestreForm() # Crea un formulario vacío para solicitudes GET (primera carga de la página)

    print("--- DEBUG (admin_trimestre_views): Preparando contexto y renderizando plantilla. ---")
    return render(request, 'mi_admin/admin_listar_trimestres.html', {
        'trimestres': trimestres,
        'form': form
    })

# El resto de tus vistas (admin_editar_trimestre, admin_eliminar_trimestre)
# no necesitan cambios si ya funcionan correctamente.


@login_required
@user_passes_test(is_administrativo, login_url='/')
def admin_editar_trimestre(request, trimestre_id):
    trimestre = get_object_or_404(Trimestre, id=trimestre_id)

    if request.method == 'POST':
        form = TrimestreForm(request.POST, instance=trimestre)
        if form.is_valid():
            form.save()
            messages.success(request, "Trimestre actualizado exitosamente.")
            return redirect('mi_admin:admin_listar_trimestres')
        else:
            messages.error(request, "Error al actualizar el trimestre. Por favor, revise los datos.")
    else:
        form = TrimestreForm(instance=trimestre)

    return render(request, 'mi_admin/admin_editar_trimestre.html', {
        'form': form,
        'trimestre': trimestre
    })

# Opcional: Vista para eliminar si la necesitas
@login_required
@user_passes_test(is_administrativo, login_url='/')
def admin_eliminar_trimestre(request, trimestre_id):
    trimestre = get_object_or_404(Trimestre, id=trimestre_id)
    if request.method == 'POST':
        trimestre.delete()
        messages.success(request, "Trimestre eliminado exitosamente.")
        return redirect('mi_admin:admin_listar_trimestres')
    # Opcionalmente, puedes renderizar una página de confirmación antes de eliminar
    return render(request, 'mi_admin/admin_confirmar_eliminar_trimestre.html', {'trimestre': trimestre})
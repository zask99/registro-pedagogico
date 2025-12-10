# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\urls.py
print(">>> MI_ADMIN/URLS.PY HA SIDO CARGADO EN ESTA EJECUCIÓN <<<")
from django.urls import path, re_path

# Define the app namespace
app_name = 'mi_admin'

# --- Importaciones de Vistas ---
from mi_admin.views.dashboard_views import dashboard

# Importa el resto de tus vistas existentes
from mi_admin.views.administrativo_views import dashboard_administrativo
from mi_admin.views.docente_views import (
    dashboard_docente,
    listar_cursos_docente,
    listar_estudiantes_por_curso_docente,
    registrar_asistencia,
)
from mi_admin.views.docente_reportes import reporte_asignacion_trimestre_pdf

from mi_admin.views.views import (
    docente_calificaciones_view,
    crear_subcomponente_evaluacion,
    guardar_nota_view,
    obtener_conteo_asistencias_ajax,
    guardar_nota_decidir,
    guardar_observacion,
    guardar_autoevaluacion,
    _recalcular_promedio_final_trimestral,
    guardar_desempeno,
    crear_evaluacion,
    editar_o_eliminar_evaluacion_subcomponente
)
from mi_admin.views.admin_registrar_persona_views import registrar_persona,importar_estudiantes_excel
from mi_admin.views.admin_listar_estudiantes import admin_listar_estudiantes
from mi_admin.views.auth_views import logout_view
from mi_admin.views.admin_admin_listar_curso import admin_listar_curso
from mi_admin.views.admin_materias import (
    assign_teacher_view,
    materias_list_view,
    api_get_materia_assignments,
    materias_create_view
)
from mi_admin.views.admin_gestion_curso_views import (
    admin_anadir_curso,
    admin_assign_materia_to_curso
)
from mi_admin.views.admin_trimestre_views import (
    admin_listar_trimestres,
    admin_editar_trimestre,
    admin_eliminar_trimestre
)
from mi_admin.views.estudiante_views import (
    dashboard_estudiante,
    ver_mis_calificaciones,
    ver_detalle_calificacion,
    listar_mis_cursos_estudiante,
    ver_mi_asistencia,
)
from mi_admin.views.selenium_bot import CargarNotasSIEView, ajax_preview_notas_view # <-- ¡Importa la nueva vista!
from mi_admin.views.api_views import api_get_course_assignments
from mi_admin.views.selenium_bot import CargarNotasSIEView
# --- DEFINICIÓN DE URLS ---
urlpatterns = [
    path('importar_estudiantes/', importar_estudiantes_excel, name='importar_estudiantes_excel'),
    # URLs de API / AJAX
    path('obtener_conteo_asistencias_ajax/', obtener_conteo_asistencias_ajax, name='obtener_conteo_asistencias_ajax'),
    path('guardar_nota_decidir/', guardar_nota_decidir, name='guardar_nota_decidir'),
    path('guardar_observacion/', guardar_observacion, name='guardar_observacion'),
    path('guardar_autoevaluacion/', guardar_autoevaluacion, name='guardar_autoevaluacion'),
    path('guardar_desempeno/', guardar_desempeno, name='guardar_desempeno'),
    path('crear_evaluacion/', crear_evaluacion, name='crear_evaluacion'),
    path('subcomponente/<int:evaluacion_id>/editar_o_eliminar/', editar_o_eliminar_evaluacion_subcomponente, name='editar_o_eliminar_evaluacion_subcomponente'),
    path('guardar_nota/', guardar_nota_view, name='guardar_nota'),
    
    # Esta es la ruta que se necesita para el funcionamiento correcto de la plantilla de calificaciones del docente.
    path('crear_subcomponente_evaluacion/', crear_subcomponente_evaluacion, name='crear_subcomponente_evaluacion'),
    
    path('api/cursos/<int:curso_id>/asignaciones/', api_get_course_assignments, name='api_get_course_assignments'),
    path('api/materias/<int:materia_id>/asignaciones/', api_get_materia_assignments, name='api_get_materia_assignments'),
    path('cargar-notas-sie/', CargarNotasSIEView.as_view(), name='vista_subir_notas_sie'),
    # Dashboards Generales
    path('', dashboard, name='main_dashboard'),
    path('dashboard/', dashboard, name='dashboard_alias'),

    # Dashboards específicos por rol
    path('dashboard-admin/', dashboard_administrativo, name='dashboard_administrativo'),
    path('dashboard/docente/', dashboard_docente, name='dashboard_docente'), # <-- Asegúrate de que el 'name' coincide

    # Gestión de Autenticación
    path('logout/', logout_view, name='logout'),

    # Gestión de Personas (Admin)
    path('registrar-persona/', registrar_persona, name='registrar_persona'),
    
    # Rutas para el CRUD de Cursos (ADMIN)
    path('cursos/', admin_listar_curso, name='admin_listar_cursos'),
    path('cursos/anadir/', admin_anadir_curso, name='admin_anadir_curso'),
    path('cursos/<int:curso_id>/estudiantes/', admin_listar_estudiantes, name='admin_listar_estudiantes'),
    path('cursos/asignar-materia/', admin_assign_materia_to_curso, name='admin_assign_materia_to_curso'),

    # Rutas para la Gestión de Trimestres (ADMIN)
    path('trimestres/', admin_listar_trimestres, name='admin_listar_trimestres'),
    path('trimestres/<int:trimestre_id>/editar/', admin_editar_trimestre, name='admin_editar_trimestre'),
    path('trimestres/<int:trimestre_id>/eliminar/', admin_eliminar_trimestre, name='admin_eliminar_trimestre'),
    
    # Rutas de Materias (Admin)
    path('materias/', materias_list_view, name='admin_materias_list'),
    path('materias/crear/', materias_create_view, name='admin_materias_create'),
    path('materias/assign_teacher/', assign_teacher_view, name='admin_materias_assign_teacher'),

    # Rutas para Cursos y Calificaciones (DOCENTE)
    path('docente/calificaciones/', docente_calificaciones_view, name='docente_calificaciones'),
    path('cursos-docente/', listar_cursos_docente, name='listar_cursos_docente'),
    path('cursos-docente/<int:curso_id>/estudiantes/', listar_estudiantes_por_curso_docente, name='listar_estudiantes_por_curso_docente'),

    # Rutas de Asistencia (Docente)
    path('asistencia/curso/<int:curso_id>/', registrar_asistencia, name='registrar_asistencia_curso'),
    path('asistencia/curso/<int:curso_id>/trimestre/<int:trimestre_id>/', registrar_asistencia, name='registrar_asistencia_trimestre'),

    # Rutas de Reportes PDF
    path('reporte-asignacion-trimestre-pdf/', reporte_asignacion_trimestre_pdf, name='reporte_asignacion_trimestre_pdf'),

    # --- ¡RUTAS PARA EL DASHBOARD Y SECCIONES ESPECÍFICAS DEL ESTUDIANTE! ---
    path('estudiante/', dashboard_estudiante, name='est_main_dashboard'),
    path('estudiante/mis-cursos/', listar_mis_cursos_estudiante, name='est_listar_mis_cursos_estudiante'),
    path('estudiante/mis-calificaciones/', ver_mis_calificaciones, name='est_ver_mis_calificaciones'),
    path('estudiante/mis-calificaciones/detalle/<int:resumen_id>/', ver_detalle_calificacion, name='est_ver_detalle_calificacion'),
    path('asistencia/curso/<int:curso_id>/', registrar_asistencia, name='registrar_asistencia'),
    path('estudiante/mi-asistencia/', ver_mi_asistencia, name='est_ver_mi_asistencia'),
    path('ajax/preview-notas/', ajax_preview_notas_view, name='ajax_preview_notas'),
]
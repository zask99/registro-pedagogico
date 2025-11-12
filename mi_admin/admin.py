# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Rol, Persona, Estudiante, Docente, Administrativo, Curso, Materia,
    Asignacion, Trimestre, Inscripcion, TipoComponente, Subcomponente,
    Evaluacion, Nota, ResumenTrimestral, Asistencia,
    DesempenoEstudiante  # <-- CORREGIDO: Se importó el modelo que faltaba
)


# ====================================================================
# Administrador para Modelos de Usuario y Roles
# ====================================================================

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # <-- CORREGIDO: Se eliminó 'descripcion'
    search_fields = ('nombre',)
    list_filter = ('nombre',)

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'rol')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'rol')
    search_fields = ('username', 'email', 'first_name', 'last_name')


# ====================================================================
# Administrador para Modelos de Perfiles (Persona, Estudiante, Docente, Administrativo)
# ====================================================================

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    # Esta sección ya estaba correcta y coincidía con el nuevo models.py
    list_display = ('nombres', 'apellidos', 'carnet', 'genero', 'departamento')
    search_fields = ('nombres', 'apellidos', 'carnet')
    list_filter = ('genero', 'departamento', 'pais')
    raw_id_fields = ('usuario',)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # Esta sección ya estaba correcta y coincidía con el nuevo models.py
    list_display = ('get_nombres', 'get_apellidos', 'codigo_estudiante', 'curso_actual')
    search_fields = ('persona__nombres', 'persona__apellidos', 'codigo_estudiante',
                     'curso_actual__grado', 'curso_actual__paralelo', 'curso_actual__niveles')
    list_filter = ('curso_actual',)
    raw_id_fields = ('persona', 'curso_actual',)

    @admin.display(description='Nombres')
    def get_nombres(self, obj):
        return obj.persona.nombres if obj.persona else ''

    @admin.display(description='Apellidos')
    def get_apellidos(self, obj):
        return obj.persona.apellidos if obj.persona else ''

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    # Esta sección ya estaba correcta y coincidía con el nuevo models.py
    list_display = ('get_nombres', 'get_apellidos', 'especialidad')
    search_fields = ('persona__nombres', 'persona__apellidos', 'especialidad')
    list_filter = ('especialidad',)
    raw_id_fields = ('persona',)

    @admin.display(description='Nombres')
    def get_nombres(self, obj):
        return obj.persona.nombres if obj.persona else ''

    @admin.display(description='Apellidos')
    def get_apellidos(self, obj):
        return obj.persona.apellidos if obj.persona else ''


@admin.register(Administrativo)
class AdministrativoAdmin(admin.ModelAdmin):
    # Esta sección ya estaba correcta y coincidía con el nuevo models.py
    list_display = ('get_nombres', 'get_apellidos', 'cargo')
    search_fields = ('persona__nombres', 'persona__apellidos', 'cargo')
    list_filter = ('cargo',)
    raw_id_fields = ('persona',)

    @admin.display(description='Nombres')
    def get_nombres(self, obj):
        return obj.persona.nombres if obj.persona else ''

    @admin.display(description='Apellidos')
    def get_apellidos(self, obj):
        return obj.persona.apellidos if obj.persona else ''

# ====================================================================
# Administrador para Modelos Académicos
# ====================================================================

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    # Esta sección ya estaba correcta y coincidía con el nuevo models.py
    list_display = ('grado', 'paralelo', 'get_niveles_display')
    search_fields = ('grado', 'paralelo', 'niveles')
    list_filter = ('niveles', 'grado')


# (Busca 'MateriaAdmin' en tu admin.py)
@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    # CORREGIDO: Reemplaza los campos anteriores por 'descripcion'
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    list_filter = () # No hay mucho que filtrar aquí
    
@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    # Esta sección ya estaba correcta y coincidía con el nuevo models.py
    list_display = ('curso', 'materia', 'docente', 'anio_academico')
    list_filter = ('curso', 'materia', 'anio_academico', 'docente')
    search_fields = ('curso__grado', 'curso__paralelo', 'curso__niveles', 
                     'materia__nombre', 'docente__persona__nombres', 'docente__persona__apellidos')
    raw_id_fields = ('curso', 'materia', 'docente')

@admin.register(Trimestre)
class TrimestreAdmin(admin.ModelAdmin):
    # Esta sección ya estaba correcta y coincidía con el nuevo models.py
    list_display = ('nombre', 'numero', 'gestion', 'fecha_inicio', 'fecha_fin')
    list_filter = ('gestion', 'numero')
    search_fields = ('nombre',)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    # <-- CORREGIDO: Se reemplazó 'fecha_inscripcion' por 'fecha_creacion'
    list_display = ('estudiante', 'curso', 'fecha_creacion', 'anio_academico')
    list_filter = ('curso', 'anio_academico')
    search_fields = ('estudiante__persona__nombres', 'estudiante__persona__apellidos',
                     'curso__grado', 'curso__paralelo', 'curso__niveles')
    raw_id_fields = ('estudiante', 'curso')


# ====================================================================
# Administrador para Modelos de Calificaciones y Asistencia
# ====================================================================

@admin.register(TipoComponente)
class TipoComponenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje_total_componente')
    search_fields = ('nombre',)

@admin.register(Subcomponente)
class SubcomponenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_componente', 'asignacion', 'trimestre', 'porcentaje_maximo')
    list_filter = (
        'tipo_componente',
        'asignacion__materia__nombre',
        'asignacion__curso__grado', 
        'trimestre'
    )
    search_fields = ('nombre', 'tipo_componente__nombre', 'asignacion__materia__nombre',
                     'asignacion__curso__grado', 'asignacion__curso__paralelo', 'asignacion__curso__niveles') 
    raw_id_fields = ('tipo_componente', 'asignacion', 'trimestre')


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'asignacion', 'trimestre', 'subcomponente', 'get_tipo_componente', 'ponderacion', 'fecha_evaluacion')
    list_filter = ('asignacion', 'trimestre', 'subcomponente__tipo_componente')
    # <-- CORREGIDO: Se reemplazó 'nombre_evaluacion' por 'nombre'
    search_fields = ('nombre', 'asignacion__materia__nombre', 'subcomponente__nombre',
                     'asignacion__curso__grado', 'asignacion__curso__paralelo', 'asignacion__curso__niveles') 
    raw_id_fields = ('asignacion', 'trimestre', 'subcomponente')

    @admin.display(description='Tipo Componente')
    def get_tipo_componente(self, obj):
        return obj.subcomponente.tipo_componente.nombre if obj.subcomponente and obj.subcomponente.tipo_componente else ''


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'evaluacion', 'nota_obtenida', 'fecha_registro')
    list_filter = ('estudiante__curso_actual__niveles', 'estudiante__curso_actual__grado', 'evaluacion__asignacion__materia', 'evaluacion__trimestre')
    # <-- CORREGIDO: Se reemplazó 'evaluacion__nombre_evaluacion' por 'evaluacion__nombre'
    search_fields = ('estudiante__persona__nombres', 'estudiante__persona__apellidos', 'evaluacion__nombre')
    raw_id_fields = ('estudiante', 'evaluacion')


@admin.register(ResumenTrimestral)
class ResumenTrimestralAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignacion', 'trimestre', 'nota_final_trimestre', 'fecha_generacion')
    list_filter = ('asignacion__materia', 'trimestre')
    search_fields = ('estudiante__persona__nombres', 'estudiante__persona__apellidos', 'asignacion__materia__nombre')
    raw_id_fields = ('estudiante', 'asignacion', 'trimestre')


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignacion', 'trimestre', 'fecha', 'asistio')
    list_filter = ('asistio', 'asignacion__materia', 'trimestre')
    search_fields = ('estudiante__persona__nombres', 'estudiante__persona__apellidos', 'asignacion__materia__nombre')
    raw_id_fields = ('estudiante', 'asignacion', 'trimestre')

# <-- CORREGIDO: Se añadió el admin para el modelo que faltaba
@admin.register(DesempenoEstudiante)
class DesempenoEstudianteAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignacion', 'trimestre', 'rango_cualitativo', 'fecha_registro')
    list_filter = ('rango_cualitativo', 'asignacion__materia', 'trimestre')
    search_fields = ('estudiante__persona__nombres', 'estudiante__persona__apellidos', 'asignacion__materia__nombre')
    raw_id_fields = ('estudiante', 'asignacion', 'trimestre')
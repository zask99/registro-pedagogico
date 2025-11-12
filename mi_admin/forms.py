print("¡¡¡Cargando mi_admin/forms.py corregido!!!") 

from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.utils import timezone

# --- 1. IMPORTACIONES DE MODELOS (ACTUALIZADO) ---
# Se importan todos los modelos, incluyendo el nuevo sistema de calificaciones
from .models import (
    Usuario, Rol, Persona, Estudiante, Docente, Administrativo, 
    Curso, Materia, Asignacion, Trimestre,
    # Modelos del nuevo sistema de calificaciones
    TipoComponente, Subcomponente, Evaluacion, Nota,
    DesempenoEstudiante, ResumenTrimestral
)

# --- Definición de clase de estilo reutilizable ---
form_input_class = 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900 bg-white dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-100'
form_select_class = form_input_class
form_textarea_class = f"{form_input_class} min-h-[80px]" # Clase para textareas
form_date_class = f"{form_input_class} text-gray-500 dark:text-gray-400" # Para que el placeholder 'yyyy-mm-dd' no sea blanco
form_number_class = form_input_class

# --- 2. FORMULARIOS DE MODELOS ACADÉMICOS (CORREGIDOS) ---

class TrimestreForm(forms.ModelForm):
    class Meta:
        model = Trimestre
        # CORREGIDO: Se añadió 'numero'
        fields = ['nombre', 'gestion', 'numero', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': form_input_class, 'placeholder': 'Ej: Primer Trimestre'}),
            'gestion': forms.NumberInput(attrs={'class': form_number_class, 'placeholder': 'Ej: 2025'}),
            # AÑADIDO: Widget para 'numero'
            'numero': forms.NumberInput(attrs={'class': form_number_class, 'placeholder': 'Ej: 1, 2 o 3'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': form_date_class}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': form_date_class}),
        }
        labels = {
            'nombre': 'Nombre del Trimestre',
            'gestion': 'Año Académico (Gestión)',
            'numero': 'Número de Trimestre',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
        }

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        # CORREGIDO: Se añadió 'anio_academico'
        fields = ['curso', 'materia', 'docente', 'anio_academico'] 
        widgets = {
            'curso': forms.Select(attrs={'class': form_select_class}),
            'materia': forms.Select(attrs={'class': form_select_class}),
            'docente': forms.Select(attrs={'class': form_select_class}),
            # AÑADIDO: Widget para 'anio_academico'
            'anio_academico': forms.NumberInput(attrs={'class': form_number_class, 'placeholder': 'Ej: 2025'}),
        }
        labels = {
            'curso': 'Curso',
            'materia': 'Materia',
            'docente': 'Docente',
            'anio_academico': 'Año Académico',
        }

# (Busca 'MateriaForm' en tu forms.py)
class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia 
        # CORREGIDO: Solo nombre y descripcion
        fields = ['nombre', 'descripcion'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': form_input_class}),
            # CORREGIDO: Widget para descripcion
            'descripcion': forms.Textarea(attrs={'class': form_textarea_class, 'rows': 3}), 
        }
        labels = {
            'nombre': 'Nombre de la Materia',
            'descripcion': 'Descripción', # CORREGIDO
        }
# --- Formulario de AsignacionMateriaDocente (Sin cambios, ya era compatible) ---
class AsignacionMateriaDocenteForm(forms.ModelForm):
    docente = forms.ModelChoiceField(
        queryset=Docente.objects.select_related('persona').order_by('persona__apellidos'), 
        empty_label="-- Seleccionar Docente --",
        widget=forms.Select(attrs={'class': form_select_class}),
        label="Docente a Asignar"
    )
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.order_by('niveles', 'grado', 'paralelo'), 
        empty_label="-- Seleccionar Curso --",
        widget=forms.Select(attrs={'class': form_select_class}),
        label="Curso"
    )
    materia = forms.ModelChoiceField(
        queryset=Materia.objects.order_by('nombre'), 
        empty_label="-- Seleccionar Materia --",
        widget=forms.Select(attrs={'class': form_select_class}),
        label="Materia"
    )
    anio_academico = forms.IntegerField(
        initial=timezone.now().year, 
        widget=forms.NumberInput(attrs={'class': form_number_class, 'placeholder': 'Ej: 2025'}),
        label="Año Académico"
    )
    class Meta:
        model = Asignacion 
        fields = ['curso', 'materia', 'docente', 'anio_academico'] 

    def clean(self):
        cleaned_data = super().clean()
        curso = cleaned_data.get('curso')
        materia = cleaned_data.get('materia')
        anio_academico = cleaned_data.get('anio_academico')
        if curso and materia and anio_academico:
            qs = Asignacion.objects.filter(
                curso=curso,
                materia=materia,
                anio_academico=anio_academico
            )
            if self.instance.pk: 
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError(
                    f"Ya existe una asignación para la materia '{materia.nombre}' en el curso '{curso.get_full_name()}' para el año académico {anio_academico}."
                )
        return cleaned_data

# --- Formulario de AsignacionDocente (Sin cambios, ya era compatible) ---
class AsignacionDocenteForm(forms.Form):
    materia_id = forms.IntegerField(widget=forms.HiddenInput())
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all().order_by('niveles', 'grado', 'paralelo'),
        empty_label="Seleccione un Curso",
        widget=forms.Select(attrs={'class': form_select_class}),
        error_messages={'required': 'Por favor, seleccione un curso.'}
    )
    docente = forms.ModelChoiceField(
        queryset=Docente.objects.all().select_related('persona').order_by('persona__apellidos', 'persona__nombres'), 
        empty_label="Seleccione un Docente",
        widget=forms.Select(attrs={'class': form_select_class}),
        error_messages={'required': 'Por favor, seleccione un docente.'}
    )
    anio_academico = forms.IntegerField(
        initial=timezone.now().year,
        min_value=2000,
        max_value=2100,
        widget=forms.NumberInput(attrs={'class': form_number_class}),
        label="Año Académico",
        error_messages={
            'required': 'Por favor, ingrese un año académico.',
            'min_value': 'El año debe ser al menos 2000.',
            'max_value': 'El año no puede ser más de 2100.',
            'invalid': 'El año académico debe ser un número válido.'
        }
    )
    def clean(self):
        cleaned_data = super().clean()
        materia_id = cleaned_data.get('materia_id')
        curso = cleaned_data.get('curso')
        anio_academico = cleaned_data.get('anio_academico')
        if materia_id is not None and curso and anio_academico is not None:
            try:
                materia = Materia.objects.get(id=materia_id)
                cleaned_data['materia'] = materia 
            except Materia.DoesNotExist:
                self.add_error('materia_id', "La materia seleccionada no es válida.")
                return cleaned_data
            if Asignacion.objects.filter(materia=materia, curso=curso, anio_academico=anio_academico).exists():
                self.add_error(None, 
                    f"La materia '{materia.nombre}' ya está asignada al curso '{curso.get_full_name()}' para el año {anio_academico}. "
                    "Por favor, elija un curso o año académico diferente."
                )
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materia_id'].required = False


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['grado', 'paralelo', 'niveles']
        widgets = {
            'grado': forms.NumberInput(attrs={'class': form_number_class, 'placeholder': 'Ej: 1, 2, ...'}),
            'paralelo': forms.TextInput(attrs={'class': form_input_class, 'placeholder': 'Ej: A, B, ...'}),
            'niveles': forms.Select(attrs={'class': form_select_class}),
        }

# --- 3. FORMULARIOS DE PERSONA/PERFIL (Sin cambios, ya eran compatibles) ---

class UsuarioForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        empty_label="Seleccione un Rol",
        required=True,
        widget=forms.Select(attrs={'class': form_select_class})
    )
    class Meta:
        model = Usuario
        fields = ('rol',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']
        if 'email' in self.fields:
            del self.fields['email']

class PersonaForm(forms.Form):
    nombres = forms.CharField(max_length=100, label="Nombres", widget=forms.TextInput(attrs={'class': form_input_class}))
    apellidos = forms.CharField(max_length=100, label="Apellidos", widget=forms.TextInput(attrs={'class': form_input_class}))
    carnet = forms.CharField(max_length=20, required=True, label="Carnet de Identidad (CI)", 
                             widget=forms.TextInput(attrs={'class': form_input_class, 'placeholder': 'Ej: 1234567LP'}))
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': form_date_class}),
        label="Fecha de Nacimiento"
    )
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    genero = forms.ChoiceField(choices=GENERO_CHOICES, required=False, label="Género", widget=forms.Select(attrs={'class': form_select_class}))
    pais = forms.CharField(max_length=100, required=False, label="País", widget=forms.TextInput(attrs={'class': form_input_class, 'value': 'Bolivia'}))
    departamento = forms.CharField(max_length=100, required=False, label="Departamento", widget=forms.TextInput(attrs={'class': form_input_class}))
    provincia = forms.CharField(max_length=100, required=False, label="Provincia", widget=forms.TextInput(attrs={'class': form_input_class}))
    localidad = forms.CharField(max_length=100, required=False, label="Localidad", widget=forms.TextInput(attrs={'class': form_input_class}))

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo_estudiante', 'curso_actual']
        widgets = {
            'codigo_estudiante': forms.TextInput(attrs={'class': form_input_class, 'placeholder': 'Código RUDE (Opcional)'}),
            'curso_actual': forms.Select(attrs={'class': form_select_class}),
        }
        labels = {
            'codigo_estudiante': 'Código RUDE',
            'curso_actual': 'Curso Actual'
        }

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['especialidad']
        widgets = {
            'especialidad': forms.TextInput(attrs={'class': form_input_class}),
        }

class AdministrativoForm(forms.ModelForm):
    class Meta:
        model = Administrativo
        fields = ['cargo']
        widgets = {
            'cargo': forms.TextInput(attrs={'class': form_input_class}),
        }


# --- 4. NUEVOS FORMULARIOS (Sistema de Calificaciones) ---
# Estos formularios no existían y son necesarios para los nuevos modelos.

class TipoComponenteForm(forms.ModelForm):
    class Meta:
        model = TipoComponente
        fields = ['nombre', 'descripcion', 'porcentaje_total_componente']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': form_input_class}),
            'descripcion': forms.Textarea(attrs={'class': form_textarea_class, 'rows': 3}),
            'porcentaje_total_componente': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre del Componente (Ej: Saber)',
            'descripcion': 'Descripción',
            'porcentaje_total_componente': 'Porcentaje Total (%)'
        }

class SubcomponenteForm(forms.ModelForm):
    class Meta:
        model = Subcomponente
        fields = ['tipo_componente', 'nombre', 'asignacion', 'trimestre', 'porcentaje_maximo', 'ponderacion_evaluacion_unica']
        widgets = {
            'tipo_componente': forms.Select(attrs={'class': form_select_class}),
            'nombre': forms.TextInput(attrs={'class': form_input_class, 'placeholder': 'Ej: Examen Bimestral, Tareas'}),
            'asignacion': forms.Select(attrs={'class': form_select_class}),
            'trimestre': forms.Select(attrs={'class': form_select_class}),
            'porcentaje_maximo': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
            'ponderacion_evaluacion_unica': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
        }
        # Puedes añadir 'labels' si quieres que sean más descriptivos

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['asignacion', 'trimestre', 'subcomponente', 'nombre', 'descripcion', 'fecha_evaluacion', 'ponderacion']
        widgets = {
            'asignacion': forms.Select(attrs={'class': form_select_class}),
            'trimestre': forms.Select(attrs={'class': form_select_class}),
            'subcomponente': forms.Select(attrs={'class': form_select_class}),
            'nombre': forms.TextInput(attrs={'class': form_input_class, 'placeholder': 'Ej: Examen Unidad 1'}),
            'descripcion': forms.Textarea(attrs={'class': form_textarea_class, 'rows': 3}),
            'fecha_evaluacion': forms.DateInput(attrs={'type': 'date', 'class': form_date_class}),
            'ponderacion': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['estudiante', 'evaluacion', 'nota_obtenida']
        widgets = {
            'estudiante': forms.Select(attrs={'class': form_select_class}),
            'evaluacion': forms.Select(attrs={'class': form_select_class}),
            'nota_obtenida': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
        }

class DesempenoEstudianteForm(forms.ModelForm):
    class Meta:
        model = DesempenoEstudiante
        fields = ['estudiante', 'asignacion', 'trimestre', 'observacion_texto', 'rango_cualitativo']
        widgets = {
            'estudiante': forms.Select(attrs={'class': form_select_class}),
            'asignacion': forms.Select(attrs={'class': form_select_class}),
            'trimestre': forms.Select(attrs={'class': form_select_class}),
            'observacion_texto': forms.Textarea(attrs={'class': form_textarea_class, 'rows': 4}),
            'rango_cualitativo': forms.Select(attrs={'class': form_select_class}),
        }

class ResumenTrimestralForm(forms.ModelForm):
    class Meta:
        model = ResumenTrimestral
        fields = [
            'estudiante', 'asignacion', 'trimestre', 
            'nota_saber', 'nota_hacer', 'nota_ser', 'nota_decidir',
            'prom_gral', 'autoeval', 'rango', 'situacion', 
            'observaciones', 'nota_final_trimestre'
        ]
        widgets = {
            'estudiante': forms.Select(attrs={'class': form_select_class}),
            'asignacion': forms.Select(attrs={'class': form_select_class}),
            'trimestre': forms.Select(attrs={'class': form_select_class}),
            'nota_saber': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
            'nota_hacer': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
            'nota_ser': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
            'nota_decidir': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
            'prom_gral': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
            'autoeval': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
            'rango': forms.TextInput(attrs={'class': form_input_class}),
            'situacion': forms.TextInput(attrs={'class': form_input_class}),
            'observaciones': forms.Textarea(attrs={'class': form_textarea_class, 'rows': 4}),
            'nota_final_trimestre': forms.NumberInput(attrs={'class': form_number_class, 'step': '0.01'}),
        }
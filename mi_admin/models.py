# C:\Users\Sdr\OneDrive\Escritorio\proyecto\registro_pegogico\mi_admin\models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from decimal import Decimal # Asegúrate de importar Decimal
import re # Para validación de carnet

# -----------------------------------------------------
# 1. GESTIÓN DE USUARIOS Y ROLES (Conservado de models.py)
# -----------------------------------------------------

class Rol(models.Model):
    """Define los roles del sistema (ej. Estudiante, Docente, Administrativo)."""
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre del rol")

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo Usuario."""
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    """Modelo de Usuario personalizado que reemplaza al User de Django."""
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    email = models.EmailField(unique=True) # Email debe ser único

    # Usamos el manager personalizado
    objects = UsuarioManager()

    # Campos requeridos para el login y 'createsuperuser'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username

# -----------------------------------------------------
# 2. PERFILES DE PERSONAS (Conservado de models.py)
# -----------------------------------------------------

def validate_carnet(value):
    """Validador para el carnet (CI) boliviano. Acepta números y extensión (ej. 1234567LP)."""
    if not re.match(r'^[0-9]+[A-Z]{0,2}$', value.upper()):
        raise ValidationError('El carnet debe contener solo números y una extensión opcional (ej. 1234567LP).')

class Persona(models.Model):
    """Datos personales comunes a todos los usuarios (Estudiantes, Docentes, Admin)."""
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='persona')
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    carnet = models.CharField(max_length=15, unique=True, validators=[validate_carnet], help_text="Cédula de Identidad (ej. 1234567LP)")
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, null=True, blank=True)
    
    # Datos de ubicación
    pais = models.CharField(max_length=50, default='Bolivia', null=True, blank=True)
    departamento = models.CharField(max_length=50, null=True, blank=True)
    provincia = models.CharField(max_length=50, null=True, blank=True)
    localidad = models.CharField(max_length=100, null=True, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.carnet})"
        
    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}"

class Estudiante(models.Model):
    """Datos específicos del Estudiante."""
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='estudiante')
    codigo_estudiante = models.CharField(max_length=20, unique=True, help_text="Código RUDE")
    curso_actual = models.ForeignKey('Curso', on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes_actuales')

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return self.persona.get_full_name()

class Docente(models.Model):
    """Datos específicos del Docente."""
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='docente')
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    # kárdex, etc.

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

    def __str__(self):
        return self.persona.get_full_name()

class Administrativo(models.Model):
    """Datos específicos del Personal Administrativo."""
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='administrativo')
    cargo = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Administrativo"
        verbose_name_plural = "Administrativos"

    def __str__(self):
        return f"{self.persona.get_full_name()} ({self.cargo})"


# -----------------------------------------------------
# 3. GESTIÓN ACADÉMICA
# -----------------------------------------------------

class Materia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    """Define los cursos (ej. 1ro de Primaria A). (Conservado de models.py)"""
    NIVEL_CHOICES = [
        ('INICIAL', 'Inicial'),
        ('PRIMARIA', 'Primaria'),
        ('SECUNDARIA', 'Secundaria'),
    ]
    
    niveles = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    grado = models.PositiveSmallIntegerField(help_text="Ej. 1, 2, 3...")
    paralelo = models.CharField(max_length=2, help_text="Ej. A, B, C...")
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        # Restricción para que no haya dos "1ro A de Primaria"
        unique_together = ('niveles', 'grado', 'paralelo') 
        ordering = ['niveles', 'grado', 'paralelo']

    def __str__(self):
        return f"{self.grado}° {self.get_niveles_display()} '{self.paralelo}'"
    
    def get_full_name(self):
        return f"{self.grado}° {self.get_niveles_display()} '{self.paralelo}'"


class Asignacion(models.Model):
    """
    Modela la relación entre un Docente, una Materia y un Curso para un año.
    (Actualizado a la versión de models2.py)
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True)
    anio_academico = models.IntegerField(default=timezone.now().year)

    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        constraints = [
            models.UniqueConstraint(fields=['curso', 'materia', 'anio_academico'], name='unique_asignacion')
        ]

    def __str__(self):
        docente_str = self.docente.persona.get_full_name() if self.docente else "Sin Docente"
        # CORREGIDO: Usar get_full_name() del modelo Curso de models.py
        return f"{self.materia.nombre} en {self.curso.get_full_name()} ({self.anio_academico}) - {docente_str}"


class Trimestre(models.Model):
    """Define los trimestres del año académico. (Actualizado a la versión de models2.py)"""
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    gestion = models.IntegerField(help_text="Año de gestión del trimestre.")
    numero = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Número de trimestre (ej. 1, 2, 3)")

    class Meta:
        verbose_name = 'Trimestre'
        verbose_name_plural = 'Trimestres'
        constraints = [
            models.UniqueConstraint(fields=['nombre', 'gestion'], name='unique_trimestre_nombre_gestion'),
            models.UniqueConstraint(fields=['numero', 'gestion'], name='unique_trimestre_numero_gestion')
        ]
        ordering = ['gestion', 'numero', 'fecha_inicio']

    def __str__(self):
        if self.numero:
            return f"Trimestre {self.numero} ({self.nombre}) - {self.gestion}"
        return f"{self.nombre} {self.gestion}"

# -----------------------------------------------------
# 4. REGISTROS (Inscripción de models.py, Asistencia de models2.py)
# -----------------------------------------------------

class Inscripcion(models.Model):
    """Registra la inscripción de un Estudiante en un Curso para un año específico. (Conservado de models.py)"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    anio_academico = models.PositiveSmallIntegerField(default=timezone.now().year)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        # Un estudiante solo puede estar inscrito una vez por año
        unique_together = ('estudiante', 'anio_academico')
        ordering = ['-anio_academico', 'estudiante__persona__apellidos']

    def __str__(self):
        return f"{self.estudiante} @ {self.curso} ({self.anio_academico})"

class Asistencia(models.Model):
    """Registra la asistencia por Asignacion (Materia/Curso). (Actualizado a la versión de models2.py)"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE)
    trimestre = models.ForeignKey('Trimestre', on_delete=models.CASCADE, help_text="Trimestre al que corresponde esta asistencia.")
    fecha = models.DateField()
    asistio = models.BooleanField(default=True)
    justificacion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        constraints = [
            UniqueConstraint(fields=['estudiante', 'asignacion', 'trimestre', 'fecha'], name='unique_asistencia')
        ]

    def __str__(self):
        status = "Presente" if self.asistio else "Ausente"
        # CORREGIDO: Usar los métodos de los modelos de models.py
        return f"{self.estudiante.persona.get_full_name()} - {self.asignacion.materia.nombre} ({self.asignacion.curso.get_full_name()} T{self.trimestre.numero}) el {self.fecha}: {status}"


# -----------------------------------------------------------------
# 5. SISTEMA DE CALIFICACIONES (NUEVO - Importado de models2.py)
# (Reemplaza al modelo 'Calificacion' de models.py)
# -----------------------------------------------------------------

class TipoComponente(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Ej: Ser, Saber, Hacer, Decidir")
    descripcion = models.TextField(blank=True, null=True)
    porcentaje_total_componente = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,
                                                       help_text="Porcentaje total que este componente aporta a la nota final (ej. Saber 35%)")
    class Meta:
        verbose_name = 'Tipo de Componente'
        verbose_name_plural = 'Tipos de Componentes'

    def __str__(self):
        return self.nombre


class Subcomponente(models.Model):
    tipo_componente = models.ForeignKey(TipoComponente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, help_text="Ej: Examen Bimestral, Tareas, Lecciones, Participación")
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE,
                                   help_text="Asignación específica (Curso-Materia-Docente-Año) a la que pertenece este subcomponente.")
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE,
                                   help_text="Trimestre específico al que pertenece este subcomponente.")
    porcentaje_maximo = models.DecimalField(max_digits=5, decimal_places=2, help_text="Valor máximo de este subcomponente (ej. 15 puntos).")
    ponderacion_evaluacion_unica = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'),
                                                       help_text="Ponderación para una evaluación única dentro de este subcomponente (si aplica).")

    class Meta:
        verbose_name = 'Subcomponente'
        verbose_name_plural = 'Subcomponentes'
        unique_together = ('tipo_componente', 'nombre', 'asignacion', 'trimestre')
        ordering = ['nombre']

    def __str__(self):
        # CORREGIDO: Usar get_full_name() del modelo Curso de models.py
        return f"{self.nombre} ({self.tipo_componente.nombre} en {self.asignacion.materia.nombre} {self.asignacion.curso.get_full_name()} T{self.trimestre.numero})"


class Evaluacion(models.Model):
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE)
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)
    subcomponente = models.ForeignKey(Subcomponente, on_delete=models.CASCADE, related_name='evaluaciones',
                                       help_text="Subcomponente al que pertenece esta evaluación.")
    nombre = models.CharField(max_length=255, help_text="Ej: Examen Unidad 1, Proyecto Final, Participación. Puede ser igual al nombre del Subcomponente si es la única evaluación.")
    descripcion = models.TextField(blank=True, null=True)
    fecha_evaluacion = models.DateField(default=timezone.now)
    ponderacion = models.DecimalField(max_digits=5, decimal_places=2, help_text="Puntos máximos que se pueden obtener en esta evaluación.")

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        unique_together = ('asignacion', 'trimestre', 'nombre', 'subcomponente')
        ordering = ['fecha_evaluacion', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.ponderacion} Pts) en {self.subcomponente.nombre}"


class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    nota_obtenida = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        constraints = [
            UniqueConstraint(fields=['estudiante', 'evaluacion'], name='unique_nota')
        ]

    def __str__(self):
        # CORREGIDO: Usar la relación con Persona para obtener el nombre
        return f"Nota de {self.estudiante.persona.get_full_name()} en {self.evaluacion.nombre}: {self.nota_obtenida}"


class DesempenoEstudiante(models.Model):
    # Opciones para el rango cualitativo
    RANGO_CHOICES = [
        ('ED', 'En Desarrollo'),       # 0-59
        ('DA', 'Desarrollo Adecuado'), # 60-69
        ('DO', 'Desarrollo Óptimo'),   # 70-89
        ('DP', 'Desarrollo Pleno'),    # 90-100
        ('N/A', 'No Aplica'),          # Para casos donde no hay nota
    ]

    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, related_name='desempenos')
    asignacion = models.ForeignKey('Asignacion', on_delete=models.CASCADE)
    trimestre = models.ForeignKey('Trimestre', on_delete=models.CASCADE)

    observacion_texto = models.TextField(blank=True, null=True, help_text="Observación detallada sobre el desempeño del estudiante para este período.")
    rango_cualitativo = models.CharField(
        max_length=20, 
        choices=RANGO_CHOICES,
        blank=True,
        null=True,
        help_text="Clasificación cualitativa del desempeño del estudiante (Ej: ED, DA, DO, DP)."
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Desempeño del Estudiante'
        verbose_name_plural = 'Desempeños de Estudiantes'
        unique_together = ('estudiante', 'asignacion', 'trimestre')
        ordering = ['estudiante', 'trimestre']

    def __str__(self):
        rango_display = dict(self.RANGO_CHOICES).get(self.rango_cualitativo, self.rango_cualitativo)
        # CORREGIDO: Usar la relación con Persona para obtener el nombre
        return (f"Desempeño de {self.estudiante.persona.get_full_name()} en {self.asignacion.materia.nombre} "
                f"({self.trimestre.nombre}): {rango_display or 'Sin Rango'}")


class ResumenTrimestral(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE)
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)
    
    nota_saber = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Nota del componente Saber.")
    nota_hacer = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Nota del componente Hacer.")
    nota_ser = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Nota del componente Ser.")
    nota_decidir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Nota del componente Decidir.")
    prom_gral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Promedio general del estudiante en esta materia para este trimestre.")
    autoeval = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Nota de autoevaluación del estudiante.")
    rango = models.CharField(max_length=50, blank=True, null=True, help_text="Rango de calificación del estudiante (ej. Excelente, Bueno).")
    situacion = models.CharField(max_length=50, blank=True, null=True, help_text="Situación del estudiante (ej. Promovido, Reprobado).")
    observaciones = models.TextField(blank=True, null=True, help_text="Observaciones generales del docente sobre el estudiante en el trimestre.")
    nota_final_trimestre = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Nota final del estudiante en esta materia para este trimestre.")
    fecha_generacion = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Resumen Trimestral'
        verbose_name_plural = 'Resúmenes Trimestrales'
        constraints = [
            UniqueConstraint(fields=['estudiante', 'asignacion', 'trimestre'], name='unique_resumen_trimestral')
        ]

    def __str__(self):
        # CORREGIDO: Usar los métodos de los modelos de models.py
        return f"Resumen de {self.estudiante.persona.get_full_name()} en {self.asignacion.materia.nombre} ({self.asignacion.curso.get_full_name()}) ({self.trimestre.nombre}): {self.nota_final_trimestre}"
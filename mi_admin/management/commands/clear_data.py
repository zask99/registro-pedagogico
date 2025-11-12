# mi_admin/management/commands/clear_data.py
from django.core.management.base import BaseCommand
from mi_admin.models import (
    Docente, Estudiante, Administrativo, Usuario,
    Curso, Materia, Rol, Trimestre, Asignacion, Inscripcion,
    Evaluacion, Nota, TipoComponente, Subcomponente, ResumenTrimestral, Asistencia
)
import os

class Command(BaseCommand):
    help = 'Clears all data from specific models in the mi_admin app.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando borrado de datos existentes...'))

        # Delete models that depend on others first, or where deletion propagates
        # It's usually safest to delete from the "leaf" models upwards,
        # or in an order that respects foreign key constraints.

        # Order of deletion matters. Delete dependent models first.
        # Example: Notas depend on Evaluacion, Evaluacion depends on Asignacion.
        # Also, Docente, Estudiante, Administrativo inherit from Persona, so deleting them
        # will delete their Persona data.
        # Usuario should be deleted after Docente/Estudiante/Administrativo if they reference it.

        try:
            self.stdout.write("Borrando datos de Asistencia...")
            Asistencia.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Asistencia borrados."))

            self.stdout.write("Borrando datos de Notas...")
            Nota.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Notas borrados."))

            self.stdout.write("Borrando datos de ResumenTrimestral...")
            ResumenTrimestral.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de ResumenTrimestral borrados."))

            self.stdout.write("Borrando datos de Evaluacion...")
            Evaluacion.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Evaluacion borrados."))

            self.stdout.write("Borrando datos de Inscripcion...")
            Inscripcion.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Inscripcion borrados."))

            self.stdout.write("Borrando datos de Asignacion...")
            Asignacion.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Asignacion borrados."))

            # Delete the specific profile models (Docente, Estudiante, Administrativo)
            # This will implicitly delete their associated Persona data.
            self.stdout.write("Borrando datos de Docentes...")
            Docente.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Docentes borrados."))

            self.stdout.write("Borrando datos de Estudiantes...")
            Estudiante.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Estudiantes borrados."))

            self.stdout.write("Borrando datos de Administrativos...")
            Administrativo.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Administrativos borrados."))

            # Now delete objects that don't depend on the ones above
            self.stdout.write("Borrando datos de Cursos...")
            Curso.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Cursos borrados."))

            self.stdout.write("Borrando datos de Materias...")
            Materia.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Materias borrados."))

            self.stdout.write("Borrando datos de Trimestres...")
            Trimestre.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Trimestres borrados."))

            self.stdout.write("Borrando datos de Subcomponentes...")
            Subcomponente.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Subcomponentes borrados."))

            self.stdout.write("Borrando datos de TipoComponente...")
            TipoComponente.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de TipoComponente borrados."))

            # Finally, delete Users and Roles (if no other models implicitly depend on them)
            self.stdout.write("Borrando datos de Usuarios...")
            Usuario.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Usuarios borrados."))

            self.stdout.write("Borrando datos de Roles...")
            Rol.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos de Roles borrados."))

            self.stdout.write(self.style.SUCCESS('\nTodos los datos especificados han sido borrados con éxito.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocurrió un error durante el borrado de datos: {e}'))
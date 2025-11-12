import datetime
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Populates the database with initial data for mi_admin app with asignaturas, docentes, estudiantes y asignaciones.'

    def handle(self, *args, **options):
        from mi_admin.models import (
            Rol, Usuario, Docente, Estudiante, Administrativo,
            Curso, Materia, Inscripcion, Asignacion
        )

        self.stdout.write(self.style.SUCCESS("Iniciando script de llenado de datos..."))

        # Roles
        roles_data = ['Administrador', 'Docente', 'Estudiante', 'Administrativo']
        roles = {}
        for rol_name in roles_data:
            rol, created = Rol.objects.get_or_create(nombre=rol_name)
            roles[rol_name] = rol
            self.stdout.write(f"Rol '{rol_name}' {'creado' if created else 'ya existe'}.")

        # Cursos (1º a 6º de Primaria)
        cursos_primaria = [f'{i}º de Primaria' for i in range(1, 7)]
        cursos = {}
        for curso_name in cursos_primaria:
            curso, created = Curso.objects.get_or_create(nombre=curso_name)
            cursos[curso_name] = curso
            self.stdout.write(f"Curso '{curso_name}' {'creado' if created else 'ya existe'}.")

        # Materias (Asignaturas)
        materias_data = [
            'Lengua española (oral y escrita)',
            'Idiomas indígenas (en regiones plurilingües)',
            'Inglés (como segunda lengua)',
            'Matemática',
            'Ciencias Naturales',
            'Vida, Tierra y Territorio (temas de medio ambiente, naturaleza, salud)',
            'Ciencias Sociales',
            'Historia, Geografía, Comunidad y Educación Cívica',
            'Ciencia, Tecnología y Producción',
            'Tecnología, oficios, introducción a la robótica y producción local',
            'Educación Física y Deportiva',
            'Educación Artística',
            'Artes plásticas, visuales, y música',
            'Valores, Espiritualidad y Religiones',
            'Ética, espiritualidad, valores comunitarios'
        ]
        materias = {}
        for materia_name in materias_data:
            materia, created = Materia.objects.get_or_create(nombre=materia_name)
            materias[materia_name] = materia
            self.stdout.write(f"Materia '{materia_name}' {'creada' if created else 'ya existe'}.")

        # Crear un docente para cada materia (nombre generado automáticamente)
        docentes = {}
        for i, materia_name in enumerate(materias_data, start=1):
            username = f"docente{i}"
            correo = f"docente{i}@colegio.com"
            nombres = f"Docente{i}"
            apellidos = "Apellido"
            ci = f"900000{i}LP"
            expedido = "LP"
            celular = f"7700000{i}"
            genero = "M" if i % 2 == 1 else "F"
            especialidad = materia_name

            # Crear usuario docente
            user, user_created = Usuario.objects.update_or_create(
                username=username,
                defaults={
                    'email': correo,
                    'rol': roles['Docente'],
                }
            )
            if user_created:
                pwd = get_random_string(10)
                user.set_password(pwd)
                user.save()
                self.stdout.write(f"Usuario {user.username} creado con contraseña: {pwd}")

            # Crear o actualizar docente
            try:
                docente = Docente.objects.get(ci=ci)
                docente.nombres = nombres
                docente.apellidos = apellidos
                docente.expedido = expedido
                docente.celular = celular
                docente.genero = genero
                docente.especialidad = especialidad
                docente.usuario = user
                docente.save()
                self.stdout.write(f"Docente {docente.nombres} actualizado.")
            except Docente.DoesNotExist:
                # Verificar correo único
                if Docente.objects.filter(correo=correo).exists():
                    self.stdout.write(self.style.WARNING(f"Correo {correo} ya existe en otro docente, no se creó el docente con CI {ci}."))
                    continue
                docente = Docente.objects.create(
                    ci=ci,
                    nombres=nombres,
                    apellidos=apellidos,
                    correo=correo,
                    expedido=expedido,
                    celular=celular,
                    genero=genero,
                    especialidad=especialidad,
                    usuario=user,
                )
                self.stdout.write(f"Docente {docente.nombres} creado.")
            docentes[materia_name] = docente

        # Crear 5 estudiantes por curso (del 1º al 6º de primaria)
        for curso_name in cursos_primaria:
            curso_obj = cursos[curso_name]
            for i in range(1, 6):  # 5 estudiantes
                username = f"{curso_name.replace('º de ', '')}_estudiante{i}"
                correo = f"{username}@colegio.com"
                nombres = f"Estudiante{i}"
                apellidos = curso_name.replace('º de ', '') + " Primaria"
                ci = f"8000{curso_name[0]}0{i}LP"  # Ejemplo CI
                expedido = "LP"
                celular = f"77123{curso_name[0]}{i}0"
                genero = "M" if i % 2 == 0 else "F"

                # Crear usuario estudiante
                user, user_created = Usuario.objects.update_or_create(
                    username=username,
                    defaults={
                        'email': correo,
                        'rol': roles['Estudiante'],
                    }
                )
                if user_created:
                    pwd = get_random_string(10)
                    user.set_password(pwd)
                    user.save()
                    self.stdout.write(f"Usuario {user.username} creado con contraseña: {pwd}")

                # Crear o actualizar estudiante
                try:
                    estudiante = Estudiante.objects.get(ci=ci)
                    estudiante.nombres = nombres
                    estudiante.apellidos = apellidos
                    estudiante.expedido = expedido
                    estudiante.celular = celular
                    estudiante.genero = genero
                    estudiante.curso_actual = curso_obj
                    estudiante.usuario = user
                    estudiante.save()
                    self.stdout.write(f"Estudiante {estudiante.nombres} actualizado.")
                except Estudiante.DoesNotExist:
                    if Estudiante.objects.filter(correo=correo).exists():
                        self.stdout.write(self.style.WARNING(f"Correo {correo} ya existe en otro estudiante, no se creó el estudiante con CI {ci}."))
                        continue
                    estudiante = Estudiante.objects.create(
                        ci=ci,
                        nombres=nombres,
                        apellidos=apellidos,
                        correo=correo,
                        expedido=expedido,
                        celular=celular,
                        genero=genero,
                        curso_actual=curso_obj,
                        usuario=user,
                    )
                    self.stdout.write(f"Estudiante {estudiante.nombres} creado.")

                # Crear inscripción si no existe
                Inscripcion.objects.get_or_create(
                    estudiante=estudiante,
                    curso=curso_obj,
                    defaults={'anio_academico': datetime.datetime.now().year}
                )

        # Vincular docentes con todos los cursos y sus materias correspondientes
        self.stdout.write("Creando asignaciones de docentes a cursos y materias...")
        for materia_name, docente in docentes.items():
            materia_obj = materias[materia_name]
            for curso in cursos.values():
                asignacion, created = Asignacion.objects.get_or_create(
                    docente=docente,
                    curso=curso,
                    materia=materia_obj
                )
                if created:
                    self.stdout.write(f"Asignación creada: Docente {docente.nombres} - Curso {curso.nombre} - Materia {materia_obj.nombre}")
                else:
                    self.stdout.write(f"Asignación ya existe: Docente {docente.nombres} - Curso {curso.nombre} - Materia {materia_obj.nombre}")

        self.stdout.write(self.style.SUCCESS("Script de llenado de datos finalizado con éxito."))
# Vincular docentes con todos los cursos y sus materias correspondientes
        self.stdout.write("Creando asignaciones de docentes a cursos y materias...")
        for materia_name, docente in docentes.items():
            materia_obj = materias[materia_name]
            for curso in cursos.values():
                asignacion, created = Asignacion.objects.get_or_create(
                    docente=docente,
                    curso=curso,
                    materia=materia_obj
                )
                if created:
                    self.stdout.write(f"Asignación creada: Docente {docente.nombres} - Curso {curso.nombre} - Materia {materia_obj.nombre}")
                else:
                    self.stdout.write(f"Asignación ya existe: Docente {docente.nombres} - Curso {curso.nombre} - Materia {materia_obj.nombre}")
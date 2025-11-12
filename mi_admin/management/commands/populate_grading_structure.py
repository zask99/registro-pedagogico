from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from mi_admin.models import TipoComponente, Subcomponente, Evaluacion, Asignacion, Trimestre

class Command(BaseCommand):
    help = 'Populates the database with the predefined grading structure (SER, SABER, HACER, DECIDIR and their evaluations).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--asignacion_id',
            type=int,
            help='ID of the Asignacion (course assignment) to link the evaluations to.',
            required=True
        )
        parser.add_argument(
            '--trimestre_id',
            type=int,
            help='ID of the Trimestre to link the evaluations to.',
            required=True
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting to populate grading structure..."))

        asignacion_id = options['asignacion_id']
        trimestre_id = options['trimestre_id']

        try:
            asignacion = Asignacion.objects.get(id=asignacion_id)
            trimestre = Trimestre.objects.get(id=trimestre_id)
        except Asignacion.DoesNotExist:
            raise CommandError(f'Asignacion with ID {asignacion_id} does not exist.')
        except Trimestre.DoesNotExist:
            raise CommandError(f'Trimestre with ID {trimestre_id} does not exist.')

        # 1. Definir los TipoComponente (SER, SABER, HACER, DECIDIR)
        componentes_nombres = ['SER', 'SABER', 'HACER', 'DECIDIR']

        # Diccionario para guardar los TipoComponente creados/obtenidos
        created_tipo_componentes = {}

        for comp_nombre in componentes_nombres:
            tipo_componente, created = TipoComponente.objects.get_or_create(
                nombre=comp_nombre
            )
            created_tipo_componentes[comp_nombre] = tipo_componente
            if created:
                self.stdout.write(self.style.SUCCESS(f"TipoComponente '{tipo_componente.nombre}' creado con éxito."))
            else:
                self.stdout.write(self.style.WARNING(f"TipoComponente '{tipo_componente.nombre}' ya existe."))

        # 2. Definir los Subcomponente y Evaluaciones

        # SER
        ser_tc = created_tipo_componentes['SER']
        sub_ser, created_sub_ser = Subcomponente.objects.get_or_create(
            tipo_componente=ser_tc,
            nombre="Evaluaciones de Ser",
            defaults={'porcentaje_maximo': 100}
        )
        if created_sub_ser:
            self.stdout.write(self.style.SUCCESS(f"Subcomponente '{sub_ser.nombre}' para SER creado."))
        else:
            self.stdout.write(self.style.WARNING(f"Subcomponente '{sub_ser.nombre}' para SER ya existe."))

        # Evaluaciones para SER
        evaluaciones_ser_data = [
            {'nombre': "Ex. Teoría Musical", 'ponderacion': 50},
            {'nombre': "Examen Práctico", 'ponderacion': 50},
        ]
        for eval_data in evaluaciones_ser_data:
            evaluacion, created = Evaluacion.objects.get_or_create(
                subcomponente=sub_ser,
                asignacion=asignacion,
                trimestre=trimestre,
                nombre_evaluacion=eval_data['nombre'],
                defaults={'ponderacion': eval_data['ponderacion']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Evaluación '{evaluacion.nombre_evaluacion}' (SER) creada.")) # Changed .INFO to .SUCCESS
            else:
                self.stdout.write(self.style.WARNING(f"  Evaluación '{evaluacion.nombre_evaluacion}' (SER) ya existe. Asegurando ponderación..."))
                if evaluacion.ponderacion != eval_data['ponderacion']:
                    evaluacion.ponderacion = eval_data['ponderacion']
                    evaluacion.save()
                    self.stdout.write(self.style.WARNING(f"  Ponderación para '{evaluacion.nombre_evaluacion}' (SER) actualizada a {evaluacion.ponderacion}."))

        # SABER
        saber_tc = created_tipo_componentes['SABER']
        sub_saber, created_sub_saber = Subcomponente.objects.get_or_create(
            tipo_componente=saber_tc,
            nombre="Evaluaciones de Saber",
            defaults={'porcentaje_maximo': 100}
        )
        if created_sub_saber:
            self.stdout.write(self.style.SUCCESS(f"Subcomponente '{sub_saber.nombre}' para SABER creado."))
        else:
            self.stdout.write(self.style.WARNING(f"Subcomponente '{sub_saber.nombre}' para SABER ya existe."))

        evaluaciones_saber_data = [
             {'nombre': "Nota Teórica (Saber)", 'ponderacion': 100},
        ]

        for eval_data in evaluaciones_saber_data:
            evaluacion, created = Evaluacion.objects.get_or_create(
                subcomponente=sub_saber,
                asignacion=asignacion,
                trimestre=trimestre,
                nombre_evaluacion=eval_data['nombre'],
                defaults={'ponderacion': eval_data['ponderacion']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Evaluación '{evaluacion.nombre_evaluacion}' (SABER) creada.")) # Changed .INFO to .SUCCESS
            else:
                self.stdout.write(self.style.WARNING(f"  Evaluación '{evaluacion.nombre_evaluacion}' (SABER) ya existe. Asegurando ponderación..."))
                if evaluacion.ponderacion != eval_data['ponderacion']:
                    evaluacion.ponderacion = eval_data['ponderacion']
                    evaluacion.save()
                    self.stdout.write(self.style.WARNING(f"  Ponderación para '{evaluacion.nombre_evaluacion}' (SABER) actualizada a {evaluacion.ponderacion}."))


        # HACER
        hacer_tc = created_tipo_componentes['HACER']
        sub_hacer, created_sub_hacer = Subcomponente.objects.get_or_create(
            tipo_componente=hacer_tc,
            nombre="Evaluaciones de Hacer",
            defaults={'porcentaje_maximo': 100}
        )
        if created_sub_hacer:
            self.stdout.write(self.style.SUCCESS(f"Subcomponente '{sub_hacer.nombre}' para HACER creado."))
        else:
            self.stdout.write(self.style.WARNING(f"Subcomponente '{sub_hacer.nombre}' para HACER ya existe."))

        evaluaciones_hacer_data = [
            {'nombre': "Tarea 1", 'ponderacion': 25},
            {'nombre': "Tarea 2", 'ponderacion': 25},
            {'nombre': "Tarea 3", 'ponderacion': 25},
            {'nombre': "Tarea 4", 'ponderacion': 25},
        ]
        for eval_data in evaluaciones_hacer_data:
            evaluacion, created = Evaluacion.objects.get_or_create(
                subcomponente=sub_hacer,
                asignacion=asignacion,
                trimestre=trimestre,
                nombre_evaluacion=eval_data['nombre'],
                defaults={'ponderacion': eval_data['ponderacion']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Evaluación '{evaluacion.nombre_evaluacion}' (HACER) creada.")) # Changed .INFO to .SUCCESS
            else:
                self.stdout.write(self.style.WARNING(f"  Evaluación '{evaluacion.nombre_evaluacion}' (HACER) ya existe. Asegurando ponderación..."))
                if evaluacion.ponderacion != eval_data['ponderacion']:
                    evaluacion.ponderacion = eval_data['ponderacion']
                    evaluacion.save()
                    self.stdout.write(self.style.WARNING(f"  Ponderación para '{evaluacion.nombre_evaluacion}' (HACER) actualizada a {evaluacion.ponderacion}."))


        # DECIDIR
        decidir_tc = created_tipo_componentes['DECIDIR']
        sub_decidir, created_sub_decidir = Subcomponente.objects.get_or_create(
            tipo_componente=decidir_tc,
            nombre="Evaluaciones de Decidir",
            defaults={'porcentaje_maximo': 100}
        )
        if created_sub_decidir:
            self.stdout.write(self.style.SUCCESS(f"Subcomponente '{sub_decidir.nombre}' para DECIDIR creado."))
        else:
            self.stdout.write(self.style.WARNING(f"Subcomponente '{sub_decidir.nombre}' para DECIDIR ya existe."))

        evaluaciones_decidir_data = [
             {'nombre': "Nota Reflexión (Decidir)", 'ponderacion': 100},
        ]
        for eval_data in evaluaciones_decidir_data:
            evaluacion, created = Evaluacion.objects.get_or_create(
                subcomponente=sub_decidir,
                asignacion=asignacion,
                trimestre=trimestre,
                nombre_evaluacion=eval_data['nombre'],
                defaults={'ponderacion': eval_data['ponderacion']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Evaluación '{evaluacion.nombre_evaluacion}' (DECIDIR) creada.")) # Changed .INFO to .SUCCESS
            else:
                self.stdout.write(self.style.WARNING(f"  Evaluación '{evaluacion.nombre_evaluacion}' (DECIDIR) ya existe. Asegurando ponderación..."))
                if evaluacion.ponderacion != eval_data['ponderacion']:
                    evaluacion.ponderacion = eval_data['ponderacion']
                    evaluacion.save()
                    self.stdout.write(self.style.WARNING(f"  Ponderación para '{evaluacion.nombre_evaluacion}' (DECIDIR) actualizada a {evaluacion.ponderacion}."))


        self.stdout.write(self.style.SUCCESS("\nGrading structure population completed successfully!"))
        self.stdout.write(self.style.WARNING("Remember to check the Django admin to verify the created components and evaluations."))
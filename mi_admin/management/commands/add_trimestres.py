# mi_admin/management/commands/add_trimestres.py
# mi_admin/management/commands/add_trimestres.py

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db import IntegrityError
from mi_admin.models import Trimestre # Import your Trimestre model

class Command(BaseCommand):
    help = 'Adds the three academic trimesters for the current year to the database.'

    def handle(self, *args, **options):
        print("DEBUG: handle method started!") # Keep this for now
        current_year = timezone.now().year
        self.stdout.write(self.style.SUCCESS(f"Attempting to add trimestres for the year: {current_year}"))

        trimestres_data = [
            {
                'nombre': 'Primer Trimestre',
                'fecha_inicio': timezone.datetime(current_year, 1, 1).date(),
                'fecha_fin': timezone.datetime(current_year, 4, 30).date(),
                'gestion': current_year
            },
            {
                'nombre': 'Segundo Trimestre',
                'fecha_inicio': timezone.datetime(current_year, 5, 1).date(),
                'fecha_fin': timezone.datetime(current_year, 8, 31).date(),
                'gestion': current_year
            },
            {
                'nombre': 'Tercer Trimestre',
                'fecha_inicio': timezone.datetime(current_year, 9, 1).date(),
                'fecha_fin': timezone.datetime(current_year, 12, 31).date(),
                'gestion': current_year
            },
        ]

        for data in trimestres_data:
            try:
                trimestre, created = Trimestre.objects.get_or_create(
                    nombre=data['nombre'],
                    gestion=data['gestion'],
                    defaults={
                        'fecha_inicio': data['fecha_inicio'],
                        'fecha_fin': data['fecha_fin']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully created: {trimestre.nombre} ({trimestre.gestion}) "
                        f"from {trimestre.fecha_inicio} to {trimestre.fecha_fin}"
                    ))
                else:
                    # ✅ ADD MORE EXPLICIT MESSAGES HERE
                    if (trimestre.fecha_inicio != data['fecha_inicio'] or
                            trimestre.fecha_fin != data['fecha_fin']):
                        trimestre.fecha_inicio = data['fecha_inicio']
                        trimestre.fecha_fin = data['fecha_fin']
                        trimestre.save()
                        self.stdout.write(self.style.WARNING(
                            f"Updated dates for existing: {trimestre.nombre} ({trimestre.gestion}). New dates: {trimestre.fecha_inicio} to {trimestre.fecha_fin}"
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"Already exists: {trimestre.nombre} ({trimestre.gestion}). Dates are already correct. No update needed."
                        ))


            except IntegrityError as e: # Catch IntegrityError specifically
                self.stderr.write(self.style.ERROR(
                    f"Error de integridad al procesar {data['nombre']} ({data['gestion']}): {e}"
                ))
            except Exception as e: # Catch any other general exception
                self.stderr.write(self.style.ERROR(
                    f"Error inesperado al procesar {data['nombre']} ({data['gestion']}): {e}"
                ))

        self.stdout.write(self.style.SUCCESS("Trimestre addition process completed."))
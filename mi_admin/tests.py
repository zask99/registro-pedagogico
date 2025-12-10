# mi_admin/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password
# ¡Asegúrate de importar Persona y Administrativo!
from mi_admin.models import (
    Usuario, Rol, Curso, Persona, Estudiante, Inscripcion, Administrativo
)

class RegistrarPersonaTest(TestCase):

    def setUp(self):
        # 1.1. Creamos los Roles
        self.rol_admin = Rol.objects.create(nombre="Administrativo")
        self.rol_estudiante = Rol.objects.create(nombre="Estudiante")
        
        # 1.2. Creamos el Curso
        self.curso = Curso.objects.create(
            grado=1, 
            paralelo="A", 
            niveles="PRIMARIA"
        )
        
        # 1.3. Creamos el usuario Administrador
        self.admin_user = Usuario.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='password123',
            rol=self.rol_admin,
            is_staff=True,
            is_superuser=True
        )
        
        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
        # 1.4. Creamos el perfil Persona para el admin
        self.admin_persona = Persona.objects.create(
            usuario=self.admin_user,
            nombres="Admin",
            apellidos="Test",
            carnet="99999" # Carnet único para el admin
        )
        
        # 1.5. Creamos el perfil Administrativo para el admin
        self.admin_profile = Administrativo.objects.create(
            persona=self.admin_persona,
            cargo="Director de Pruebas"
        )
        # --- FIN DE LA CORRECCIÓN ---
        
        # 1.6. Creamos el Cliente de Pruebas
        self.client = Client()
        
        # 1.7. Inicia sesión el administrador
        self.client.login(username='admin_test', password='password123')
        
        # 1.8. Definimos la URL a probar
        self.url = reverse('mi_admin:registrar_persona')

    # ... (La función test_registrar_estudiante_exitoso se queda igual) ...
    def test_registrar_estudiante_exitoso(self):
        """
        Prueba el flujo de control (camino 'estudiante') de la vista 
        registrar_persona.
        """
        
        # 2.1. Datos del formulario
        post_data = {
            'usuario-rol': self.rol_estudiante.id,
            'usuario-email': 'test.estudiante@colegio.com',
            'persona-nombres': 'Nombre Test',
            'persona-apellidos': 'Apellido Test',
            'persona-carnet': '1234567',
            'persona-fecha_nacimiento': '2010-01-01',
            'persona-genero': 'M',
            'persona-pais': 'Bolivia',
            'estudiante-codigo_estudiante': 'RUDE-12345',
            'estudiante-curso_actual': self.curso.id,
            'docente-especialidad': '',
            'administrativo-cargo': ''
        }

        # 2.2. Ejecutar la vista con un POST
        response = self.client.post(self.url, data=post_data)
        
        # 2.3. Verificación de la Respuesta
        self.assertEqual(response.status_code, 302)
        
        # Ahora el assertRedirects podrá seguir la redirección
        # y la página del dashboard cargará con éxito (Código 200)
        self.assertRedirects(response, reverse('mi_admin:dashboard_administrativo'))

        # 2.4. Verificación de la Base de Datos
        self.assertTrue(Usuario.objects.filter(username='RUDE-12345').exists())
        user = Usuario.objects.get(username='RUDE-12345')
        self.assertEqual(user.rol, self.rol_estudiante)
        self.assertTrue(check_password('1234567', user.password))
        self.assertTrue(Persona.objects.filter(carnet='1234567').exists())
        self.assertTrue(Estudiante.objects.filter(codigo_estudiante='RUDE-12345').exists())
        self.assertTrue(Inscripcion.objects.filter(
            estudiante__codigo_estudiante='RUDE-12345',
            curso=self.curso
        ).exists())
        
     # mi_admin/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from decimal import Decimal
from datetime import date

# Importa TODOS los modelos necesarios para el test
from mi_admin.models import (
    Usuario, Rol, Curso, Persona, Estudiante, Inscripcion, Administrativo,
    Docente, Materia, Asignacion, Trimestre, TipoComponente, 
    Subcomponente, Evaluacion, Nota, Asistencia, ResumenTrimestral
)

# ... (Tu clase RegistrarPersonaTest puede ir aquí) ...
class RegistrarPersonaTest(TestCase):
    pass


# --- TEST PARA CALIFICACIONES CORREGIDO ---

class DocenteCalificacionesViewTest(TestCase):

    def setUp(self):
        """
        Configura una base de datos de prueba completa con todos los modelos
        necesarios para la vista de calificaciones.
        """
        
        # 1. Roles
        self.rol_docente = Rol.objects.create(nombre="Docente")
        self.rol_estudiante = Rol.objects.create(nombre="Estudiante")
        
        # 2. Curso y Materia
        self.curso = Curso.objects.create(
            niveles="SECUNDARIA", 
            grado=1, 
            paralelo="A"
        )
        self.materia = Materia.objects.create(nombre="Ciencias")

        # 3. Docente (Usuario, Persona, Docente)
        self.docente_user = Usuario.objects.create_user(
            username='docente_test',
            email='docente@test.com',
            password='password123',
            rol=self.rol_docente
        )
        self.docente_persona = Persona.objects.create(
            usuario=self.docente_user,
            nombres="Profesor",
            apellidos="Prueba",
            carnet="987654"
        )
        self.docente = Docente.objects.create(
            persona=self.docente_persona,
            especialidad="Biología"
        )
        
        # 4. Asignacion (Vínculo Docente-Curso-Materia)
        self.asignacion = Asignacion.objects.create(
            curso=self.curso,
            materia=self.materia,
            docente=self.docente,
            anio_academico=2025
        )

        # 5. Trimestre
        self.trimestre = Trimestre.objects.create(
            nombre="Primer Trimestre",
            fecha_inicio=date(2025, 2, 1),
            fecha_fin=date(2025, 5, 1),
            gestion=2025,
            numero=1
        )
        
        # 6. Estudiantes (2 estudiantes para probar ranking)
        
        # Estudiante 1 (Buenas notas)
        user_est1 = Usuario.objects.create_user(username='est1', email='est1@test.com', password='111', rol=self.rol_estudiante)
        pers_est1 = Persona.objects.create(usuario=user_est1, nombres="Estudiante", apellidos="AAA Primero", carnet="111")
        self.est1 = Estudiante.objects.create(persona=pers_est1, codigo_estudiante="RUDE-111", curso_actual=self.curso)
        Inscripcion.objects.create(estudiante=self.est1, curso=self.curso, anio_academico=2025)

        # Estudiante 2 (Notas bajas)
        user_est2 = Usuario.objects.create_user(username='est2', email='est2@test.com', password='222', rol=self.rol_estudiante)
        pers_est2 = Persona.objects.create(usuario=user_est2, nombres="Estudiante", apellidos="ZZZ Segundo", carnet="222")
        self.est2 = Estudiante.objects.create(persona=pers_est2, codigo_estudiante="RUDE-222", curso_actual=self.curso)
        Inscripcion.objects.create(estudiante=self.est2, curso=self.curso, anio_academico=2025)

        # 7. Componentes (Dimensiones)
        self.comp_saber = TipoComponente.objects.create(nombre="Saber", porcentaje_total_componente=35)
        self.comp_hacer = TipoComponente.objects.create(nombre="Hacer", porcentaje_total_componente=35)
        self.comp_ser = TipoComponente.objects.create(nombre="Ser", porcentaje_total_componente=10)
        self.comp_decidir = TipoComponente.objects.create(nombre="Decidir", porcentaje_total_componente=10)
        
        # 8. Evaluaciones (Columnas de notas)
        sub_saber1 = Subcomponente.objects.create(tipo_componente=self.comp_saber, nombre="Examen 1", asignacion=self.asignacion, trimestre=self.trimestre, porcentaje_maximo=10)
        self.eval_saber1 = Evaluacion.objects.create(asignacion=self.asignacion, trimestre=self.trimestre, subcomponente=sub_saber1, nombre="Examen 1", ponderacion=Decimal('40.00'))
        
        sub_saber2 = Subcomponente.objects.create(tipo_componente=self.comp_saber, nombre="Tarea 1", asignacion=self.asignacion, trimestre=self.trimestre, porcentaje_maximo=10)
        self.eval_saber2 = Evaluacion.objects.create(asignacion=self.asignacion, trimestre=self.trimestre, subcomponente=sub_saber2, nombre="Tarea 1", ponderacion=Decimal('60.00'))

        sub_hacer1 = Subcomponente.objects.create(tipo_componente=self.comp_hacer, nombre="Proyecto", asignacion=self.asignacion, trimestre=self.trimestre, porcentaje_maximo=10)
        self.eval_hacer1 = Evaluacion.objects.create(asignacion=self.asignacion, trimestre=self.trimestre, subcomponente=sub_hacer1, nombre="Proyecto", ponderacion=Decimal('100.00'))

        # 9. Notas (Datos en las celdas)
        # Estudiante 1
        Nota.objects.create(estudiante=self.est1, evaluacion=self.eval_saber1, nota_obtenida=Decimal('8.00')) # 8 * 40%
        Nota.objects.create(estudiante=self.est1, evaluacion=self.eval_saber2, nota_obtenida=Decimal('7.00')) # 7 * 60%
        Nota.objects.create(estudiante=self.est1, evaluacion=self.eval_hacer1, nota_obtenida=Decimal('9.00')) # 9 * 100%
        
        # Estudiante 2
        Nota.objects.create(estudiante=self.est2, evaluacion=self.eval_saber1, nota_obtenida=Decimal('5.00')) # 5 * 40%
        Nota.objects.create(estudiante=self.est2, evaluacion=self.eval_saber2, nota_obtenida=Decimal('4.00')) # 4 * 60%
        Nota.objects.create(estudiante=self.est2, evaluacion=self.eval_hacer1, nota_obtenida=Decimal('6.00')) # 6 * 100%

        # 10. Asistencia (Para calcular la nota 'Ser')
        fechas_clase = [date(2025, 3, i) for i in range(1, 11)]
        
        for fecha in fechas_clase[:8]:
            Asistencia.objects.create(estudiante=self.est1, asignacion=self.asignacion, trimestre=self.trimestre, fecha=fecha, asistio=True)
        for fecha in fechas_clase[8:]:
            Asistencia.objects.create(estudiante=self.est1, asignacion=self.asignacion, trimestre=self.trimestre, fecha=fecha, asistio=False)

        for fecha in fechas_clase[:5]:
            Asistencia.objects.create(estudiante=self.est2, asignacion=self.asignacion, trimestre=self.trimestre, fecha=fecha, asistio=True)
        for fecha in fechas_clase[5:]:
            Asistencia.objects.create(estudiante=self.est2, asignacion=self.asignacion, trimestre=self.trimestre, fecha=fecha, asistio=False)

        # 11. Resumen (Para 'Decidir' y 'Autoeval')
        ResumenTrimestral.objects.create(
            estudiante=self.est1, 
            asignacion=self.asignacion, 
            trimestre=self.trimestre, 
            nota_decidir=Decimal('10.00'), 
            autoeval=Decimal('9.00')
        )
        ResumenTrimestral.objects.create(
            estudiante=self.est2, 
            asignacion=self.asignacion, 
            trimestre=self.trimestre, 
            nota_decidir=Decimal('7.00'), 
            autoeval=Decimal('7.00')
        )
        
        # 12. Cliente y URL
        self.client = Client()
        self.client.login(username='docente_test', password='password123')
        
        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
        # El nombre en tu urls.py es 'docente_calificaciones'
        self.url = reverse('mi_admin:docente_calificaciones')
        # --- FIN DE LA CORRECCIÓN ---


    def test_calificaciones_view_calculates_correctly(self):
        """
        Prueba que la vista GET calcule correctamente todos los promedios,
        asistencia, nota final, situación y ranking.
        """
        
        # --- 1. Valores Esperados (Cálculo Manual) ---
        
        # Estudiante 1:
        # Saber: (8.0 * 40) + (7.0 * 60) / (40 + 60) = (320 + 420) / 100 = 7.4
        # Hacer: (9.0 * 100) / 100 = 9.0
        # Ser:   8 / 10 días = 80% => Nota 8.0
        # Decidir: 10.0 (de setUp)
        # Autoeval: 9.0 (de setUp)
        # FINAL (Suma directa según _recalcular_...): 7.4 + 9.0 + 8.0 + 10.0 + 9.0 = 43.4
        # Situación: Reprobado (< 51)
        # Rango: 1 (mejor nota)
        
        # Estudiante 2:
        # Saber: (5.0 * 40) + (4.0 * 60) / (40 + 60) = (200 + 240) / 100 = 4.4
        # Hacer: (6.0 * 100) / 100 = 6.0
        # Ser:   5 / 10 días = 50% => Nota 5.0
        # Decidir: 7.0 (de setUp)
        # Autoeval: 7.0 (de setUp)
        # FINAL (Suma directa): 4.4 + 6.0 + 5.0 + 7.0 + 7.0 = 29.4
        # Situación: Reprobado (< 51)
        # Rango: 2 (peor nota)

        # --- 2. Ejecutar la Vista ---
        response = self.client.get(self.url, {
            'asignacion': self.asignacion.id, 
            'trimestre': self.trimestre.id
        })
        
        # --- 3. Verificaciones de la Respuesta ---
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mi_admin/docente_calificaciones.html')
        
        self.assertIn('estudiantes_data', response.context)
        est_data = response.context['estudiantes_data']
        self.assertEqual(len(est_data), 2)
        
        est1_data = est_data[0]
        est2_data = est_data[1]

        # --- 4. Verificaciones (Estudiante 1: AAA Primero) ---
        self.assertEqual(est1_data['nombre_completo'], "Estudiante AAA Primero")
        self.assertEqual(est1_data['prom_saber'], 7.4)
        self.assertEqual(est1_data['prom_hacer'], 9.0)
        self.assertEqual(est1_data['nota_ser'], 8.0)
        self.assertEqual(est1_data['nota_decidir'], 10.0)
        self.assertEqual(est1_data['autoeval'], 9.0)
        self.assertEqual(est1_data['asistencia'], "80.00% (8/10)")
        self.assertEqual(est1_data['prom_trim'], 43.4)
        self.assertEqual(est1_data['situacion'], "Reprobado")
        self.assertEqual(est1_data['rango'], 1) 
        
        # --- 5. Verificaciones (Estudiante 2: ZZZ Segundo) ---
        self.assertEqual(est2_data['nombre_completo'], "Estudiante ZZZ Segundo")
        self.assertEqual(est2_data['prom_saber'], 4.4)
        self.assertEqual(est2_data['prom_hacer'], 6.0)
        self.assertEqual(est2_data['nota_ser'], 5.0)
        self.assertEqual(est2_data['nota_decidir'], 7.0)
        self.assertEqual(est2_data['autoeval'], 7.0)
        self.assertEqual(est2_data['asistencia'], "50.00% (5/10)")
        self.assertEqual(est2_data['prom_trim'], 29.4)
        self.assertEqual(est2_data['situacion'], "Reprobado")
        self.assertEqual(est2_data['rango'], 2)

        # --- 6. Verificación de la Base de Datos ---
        resumen1 = ResumenTrimestral.objects.get(estudiante=self.est1)
        self.assertAlmostEqual(resumen1.nota_saber, Decimal('7.40'))
        self.assertAlmostEqual(resumen1.nota_hacer, Decimal('9.00'))
        self.assertAlmostEqual(resumen1.nota_ser, Decimal('8.00'))
        self.assertAlmostEqual(resumen1.nota_final_trimestre, Decimal('43.40'))
        self.assertEqual(resumen1.situacion, "Reprobado")
        self.assertEqual(resumen1.rango, "1") 

        resumen2 = ResumenTrimestral.objects.get(estudiante=self.est2)
        self.assertAlmostEqual(resumen2.nota_saber, Decimal('4.40'))
        self.assertAlmostEqual(resumen2.nota_hacer, Decimal('6.00'))
        self.assertAlmostEqual(resumen2.nota_ser, Decimal('5.00'))
        self.assertAlmostEqual(resumen2.nota_final_trimestre, Decimal('29.40'))
        self.assertEqual(resumen2.situacion, "Reprobado")
        self.assertEqual(resumen2.rango, "2")
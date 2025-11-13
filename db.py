import os
import sys
import environ # Necesitas: pip install django-environ o python-dotenv
from pathlib import Path

# Configuración básica (Asegúrate de que coincida con tu settings.py)
DB_NAME = "bd_registro_pedagogico"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
BACKUP_FILE = "respaldo_db.sql"

# Intentamos leer la contraseña del entorno, si no, la pedirá el sistema
# (O puedes escribirla aquí si es segura tu PC local)
os.environ['PGPASSWORD'] = '22213412' # <--- Pon aquí la contraseña de LA PC DONDE ESTÉS

def exportar():
    print(f"📦 Exportando base de datos '{DB_NAME}' a '{BACKUP_FILE}'...")
    # Comando para guardar (Dump)
    comando = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} --clean --if-exists {DB_NAME} > {BACKUP_FILE}"
    
    if os.system(comando) == 0:
        print("✅ ¡Exportación exitosa! Ahora haz: git add . / git commit / git push")
    else:
        print("❌ Error al exportar. Asegúrate de que PostgreSQL esté en tu PATH.")

def importar():
    print(f"⚠️  PELIGRO: Esto BORRARÁ la base de datos local '{DB_NAME}' y cargará el respaldo.")
    confirmacion = input("¿Estás seguro? Escribe 'si' para continuar: ")
    if confirmacion != 'si':
        print("Cancelado.")
        return

    print(f"📥 Importando desde '{BACKUP_FILE}'...")
    # Comando para cargar (Restore)
    comando = f"psql -U {DB_USER} -h {DB_HOST} -p {DB_PORT} -d {DB_NAME} -f {DB_FILE}"
    # Nota: En Windows a veces psql necesita redirección diferente, intentemos esta:
    comando = f"psql -U {DB_USER} -h {DB_HOST} -p {DB_PORT} {DB_NAME} < {BACKUP_FILE}"

    if os.system(comando) == 0:
        print("✅ ¡Importación exitosa! Tu base de datos es un clon de la otra.")
    else:
        print("❌ Error. Verifica que el archivo .sql exista y PostgreSQL esté instalado.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python db.py [exportar|importar]")
    elif sys.argv[1] == "exportar":
        exportar()
    elif sys.argv[1] == "importar":
        importar()
    else:
        print("Comando no reconocido.")
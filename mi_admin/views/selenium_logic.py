# Importamos las librerías necesarias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options # <--- NUEVO IMPORT
import time

def ejecutar_bot_sie(username, password, notas, curso_nombre, materia_nombre):
    print(f"Iniciando bot para {username}...")
    
    # 1. CONFIGURACIÓN PARA MANTENER ABIERTO
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) # ¡La clave mágica!

    # Iniciamos el driver con las opciones
    driver = webdriver.Chrome(options=chrome_options) 
    
    try:
        driver.get("https://academico.sie.gob.bo/") 
        
        wait = WebDriverWait(driver, 10) 

        # --- LOGIN ---
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//input[@type='checkbox']").click()
        driver.find_element(By.CLASS_NAME, "btn-aceptar").click()
        
        # --- VERIFICACIÓN DE LOGIN ---
        try:
            error_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'El usuario y/o la contraseña que ha introducido no son válidos')]"))
            )
            error_text = error_message.text
            print(f"Error de login: {error_text}")
            
            # OJO: Si hay error de login, AQUÍ SÍ cerramos para no dejar basura
            driver.quit() 
            return f"Error: Credenciales inválidas. {error_text}"

        except TimeoutException:
            print("Login exitoso.")
            pass 

        # --- NAVEGACIÓN ---
        print(f"Navegando a {curso_nombre} - {materia_nombre}...")
        time.sleep(5) 

        # --- SUBIDA DE NOTAS ---
        print("Iniciando subida de notas...")
        for estudiante in notas:
            print(f"Procesando: {estudiante['nombre']} (CI: {estudiante['ci']}) - Nota: {estudiante['nota_final']}")
            # Aquí tu lógica de llenado...
            time.sleep(0.5)
            
        print("¡Carga completada!")
        
        return "Notas subidas con éxito. El navegador sigue abierto."

    except Exception as e:
        print(f"Error fatal en Selenium: {e}")
        # En caso de error grave, quizás prefieras no cerrar para ver qué pasó
        # driver.quit() 
        return f"Error inesperado: {e}"
        
    # finally:
        # driver.quit()  <--- COMENTADO O BORRADO PARA QUE NO CIERRE
        # print("Navegador cerrado.")
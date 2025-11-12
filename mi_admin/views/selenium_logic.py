# Importamos las librerías necesarias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def ejecutar_bot_sie(username, password, notas, curso_nombre, materia_nombre):
    """
    Esta es la función que contiene toda la lógica de Selenium.
    Recibe las credenciales y los datos, no sabe nada de Django.
    ¡Ahora incluye verificación de login!
    """
    print(f"Iniciando bot para {username}...")
    
    # Selenium Manager gestiona el driver automáticamente
    driver = webdriver.Chrome() 
    
    try:
        driver.get("https://academico.sie.gob.bo/") # URL Real
        
        # Espera hasta 10 segundos a que los elementos carguen
        wait = WebDriverWait(driver, 10) 

        # 1. LOGIN
        # Usamos wait.until() para asegurarnos de que los campos estén listos
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//input[@type='checkbox']").click()
        driver.find_element(By.CLASS_NAME, "btn-aceptar").click()
        
        # -----------------------------------------------------------------
        # ¡LÓGICA NUEVA! VERIFICACIÓN DE LOGIN
        # -----------------------------------------------------------------
        try:
            # Damos 3 segundos para que la página reaccione (muestre error o cargue el dashboard)
            # Esperamos a que aparezca el MENSAJE DE ERROR
            error_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'El usuario y/o la contraseña que ha introducido no son válidos')]"))
            )
            
            # Si lo encontramos, el login falló. Devolvemos el error.
            error_text = error_message.text
            print(f"Error de login detectado: {error_text}")
            return f"Error: Credenciales inválidas. El sistema dijo: '{error_text}'"

        except TimeoutException:
            # ¡Perfecto! Si después de 3 segundos NO se encontró el mensaje de error,
            # significa que el login fue exitoso.
            print("Login exitoso. No se encontró mensaje de error.")
            pass # El script continúa...
        # -----------------------------------------------------------------
        # FIN DE LA LÓGICA NUEVA
        # -----------------------------------------------------------------

        
        # 2. NAVEGACIÓN
        # (Esta parte es un EJEMPLO. Debes ajustarla a los clics
        # reales que haces en el SIE para llegar a la página de notas)
        print(f"Navegando a {curso_nombre} - {materia_nombre}...")
        
        # (Aquí va tu código para hacer clic en menús, etc.)
        # Ejemplo:
        # wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Recibidos"))).click()
        # wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Unidad Educativa"))).click()
        # ...etc...

        # Simulación de navegación (BORRA ESTO CUANDO IMPLEMENTES LO REAL)
        time.sleep(5) 

        # 3. SUBIDA DE NOTAS
        print("Iniciando subida de notas...")
        for estudiante in notas:
            print(f"Procesando: {estudiante['nombre']} (CI: {estudiante['ci']}) - Nota: {estudiante['nota_final']}")
            
            # (Aquí va tu lógica real para encontrar el <input> del estudiante y poner la nota)
            # Ejemplo:
            # campo_nota = wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[td[contains(text(), '{estudiante['ci']}')]]//input[@type='text']")))
            # campo_nota.clear()
            # campo_nota.send_keys(str(estudiante['nota_final']))
            
            time.sleep(0.5) # Pausa entre cada estudiante
            
        print("¡Carga completada!")
        
        return "Notas subidas con éxito."

    except Exception as e:
        # Captura cualquier otro error (ej. no se encontró un botón)
        print(f"Error fatal en Selenium: {e}")
        # Guarda una captura de pantalla para depurar
        driver.save_screenshot('error_bot_sie.png')
        return f"Error inesperado en Selenium: {e}"
        
    finally:
        # Asegúrate de que el navegador siempre se cierre
        driver.quit()
        print("Navegador cerrado.")
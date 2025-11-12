# mi_admin/permissions.py

def is_administrativo(user):
    print(f"--- DEBUG (permissions): Verificando permisos para usuario: {user.username} ---")
    if not user.is_authenticated:
        print("--- DEBUG (permissions): Usuario NO autenticado. Retornando False. ---")
        return False

    if not hasattr(user, 'rol') or user.rol is None:
        print("--- DEBUG (permissions): Usuario NO tiene atributo 'rol' o 'rol' es None. Retornando False. ---")
        return False

    # --- INICIO DE LA CORRECCIÓN ---
    rol_nombre_lower = user.rol.nombre.lower().strip() # <--- Añadido .strip()
    # --- FIN DE LA CORRECCIÓN ---
    print(f"--- DEBUG (permissions): Rol del usuario detectado (limpio): '{rol_nombre_lower}' ---")

    expected_rol_lower = 'administrativo' 

    is_admin = (rol_nombre_lower == expected_rol_lower)
    print(f"--- DEBUG (permissions): ¿Coincide el rol con '{expected_rol_lower}'? {is_admin} ---")

    return is_admin

def is_docente(user):
    print(f"--- DEBUG (permissions): Verificando permisos para usuario: {user.username} (is_docente) ---")
    if not user.is_authenticated:
        print("--- DEBUG (permissions): Usuario NO autenticado. Retornando False. ---")
        return False
    if not hasattr(user, 'rol') or user.rol is None:
        print("--- DEBUG (permissions): Usuario NO tiene atributo 'rol' o 'rol' es None. Retornando False. ---")
        return False

    # --- INICIO DE LA CORRECCIÓN ---
    rol_nombre_lower = user.rol.nombre.lower().strip() # <--- Añadido .strip()
    # --- FIN DE LA CORRECCIÓN ---
    print(f"--- DEBUG (permissions): Rol del usuario detectado (limpio): '{rol_nombre_lower}' ---")

    expected_rol_lower = 'docente' 

    is_teacher = (rol_nombre_lower == expected_rol_lower)
    print(f"--- DEBUG (permissions): ¿Coincide el rol con '{expected_rol_lower}'? {is_teacher} ---")
    return is_teacher

def is_estudiante(user):
    print(f"--- DEBUG (permissions): Verificando permisos para usuario: {user.username} (is_estudiante) ---")
    if not user.is_authenticated:
        print("--- DEBUG (permissions): Usuario NO autenticado. Retornando False. ---")
        return False
    if not hasattr(user, 'rol') or user.rol is None:
        print("--- DEBUG (permissions): Usuario NO tiene atributo 'rol' o 'rol' es None. Retornando False. ---")
        return False

    # --- INICIO DE LA CORRECCIÓN ---
    rol_nombre_lower = user.rol.nombre.lower().strip() # <--- Añadido .strip()
    # --- FIN DE LA CORRECCIÓN ---
    print(f"--- DEBUG (permissions): Rol del usuario detectado (limpio): '{rol_nombre_lower}' ---")

    expected_rol_lower = 'estudiante' 

    is_student = (rol_nombre_lower == expected_rol_lower)
    print(f"--- DEBUG (permissions): ¿Coincide el rol con '{expected_rol_lower}'? {is_student} ---")
    return is_student
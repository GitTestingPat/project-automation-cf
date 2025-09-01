import requests
import pytest
import time
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-06: Crear usuario como admin (POST /users/)
Objetivo: Verificar que un usuario autenticado como admin pueda crear un nuevo usuario.
"""

def get_admin_token():
    """
    Intenta obtener un token JWT para un usuario administrador.
    Si las credenciales fallan, se lanza una PermissionError.
    """
    # Datos de un usuario administrador conocido.
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        # Lanzar una excepción personalizada para que la prueba pueda manejarla
        raise PermissionError(f"Falló el login de admin. Status: {response.status_code}, Body: {response.text}")

def test_create_user_as_admin():
    """
    TC-API-06: Crear usuario como admin.
    """
    # 1. Intentar obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        # Si no se puede obtener el token, se salta la prueba
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Preparar datos para el nuevo usuario
    # Generar un email único para evitar conflictos
    timestamp = int(time.time())
    new_user_email = f"new_user_{timestamp}@test.com"
    new_user_data = {
        "email": new_user_email,
        "password": "SecurePass123!",
        "full_name": f"New User {timestamp}",
        "role": "passenger"
    }

    # 3. Hacer la solicitud POST a /users/
    response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=headers)

    # 4. Verificar el código de estado.
    # Si el servidor devuelve 500, es probable un fallo interno de la API de prueba.
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear un usuario. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # Verificar que la creación sea exitosa (201 Created)
    assert response.status_code == 201, (
        f"Error al crear usuario como admin. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 5. Validar la estructura del usuario creado (esquema UserOut)
    created_user = response.json()
    assert isinstance(created_user, dict), f"Se esperaba un diccionario, se obtuvo {type(created_user)}"

    # Verificaciones básicas del esquema UserOut
    assert "id" in created_user, "Falta 'id' en el usuario creado"
    assert "email" in created_user, "Falta 'email' en el usuario creado"
    assert created_user["email"] == new_user_email, (
        f"El email del usuario creado no coincide. "
        f"Esperado: {new_user_email}, Obtenido: {created_user['email']}"
    )
    assert "full_name" in created_user, "Falta 'full_name' en el usuario creado"
    # El campo 'role' es opcional en UserOut, pero si está, debe ser válido
    if "role" in created_user:
         assert created_user["role"] in ["passenger", "admin"], f"Rol inválido: {created_user['role']}"

    print(f"✅ Usuario creado exitosamente como admin. ID: {created_user['id']}, Email: {created_user['email']}")

import requests
import pytest
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-07: Obtener mi perfil (GET /users/me/)
Objetivo: Verificar que un usuario autenticado pueda obtener su propia información de perfil.
"""

def get_valid_user_token():
    """
    Obtiene un token JWT para un usuario registrado.
    Reutiliza las credenciales conocidas que funcionan para login.
    """
    # Datos de un usuario registrado que se sabe válido.
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    # Verificar login exitoso para continuar
    assert response.status_code == 200, (
        f"Falló el login del usuario. Status: {response.status_code}, Body: {response.text}"
    )

    token_data = response.json()
    return token_data["access_token"]

def test_get_my_profile():
    """
    TC-API-07: Obtener mi perfil.
    """
    # 1. Obtener token de autenticación
    token = get_valid_user_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Hacer la solicitud GET a /users/me/
    response = requests.get(f"{BASE_URL}/users/me/", headers=headers)

    # 3. Verificar que la respuesta sea exitosa (200 OK)
    # Manejar el posible error 500 del servidor de la API de prueba
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar obtener el perfil. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    assert response.status_code == 200, (
        f"Error al obtener el perfil del usuario. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 4. Validar la estructura del perfil del usuario (esquema UserOut)
    user_profile = response.json()
    assert isinstance(user_profile, dict), f"Se esperaba un diccionario, se obtuvo {type(user_profile)}"

    # Verificaciones básicas del esquema UserOut
    assert "id" in user_profile, "Falta 'id' en el perfil del usuario"
    assert "email" in user_profile, "Falta 'email' en el perfil del usuario"
    assert "@" in user_profile["email"], "El 'email' no tiene un formato válido"
    assert "full_name" in user_profile, "Falta 'full_name' en el perfil del usuario"
    # Verificar campo 'role' válido
    if "role" in user_profile:
        assert user_profile["role"] in ["passenger", "admin"], f"Rol inválido: {user_profile['role']}"

    print(f"✅ Perfil obtenido exitosamente. ID: {user_profile['id']}, Email: {user_profile['email']}, "
          f"Nombre: {user_profile['full_name']}")

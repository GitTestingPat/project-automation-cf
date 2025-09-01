import requests
import pytest
import time
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-09: Eliminar usuario (DELETE /users/{user_id})
Objetivo: Verificar que un usuario autenticado como admin pueda eliminar a otro usuario.
"""

def get_admin_token():
    """
    Intenta obtener un token JWT para un usuario administrador.
    Si las credenciales fallan, se lanza una PermissionError.
    """
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        raise PermissionError(f"Falló el login de admin. Status: {response.status_code}, Body: {response.text}")


def create_test_user_for_deletion(admin_token):
    """
    Crea un usuario de prueba específico para ser eliminado.
    Asegura trabajar con un usuario controlado.
    Devuelve el ID del usuario creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    timestamp = int(time.time())
    user_data = {
        "email": f"delete_test_{timestamp}@test.com",
        "password": "ToDeletePass123!",
        "full_name": f"User to Delete {timestamp}",
        "role": "passenger"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=headers)

    if response.status_code == 201:
        # Éxito: Devolver el ID del usuario creado
        response_data = response.json()
        return response_data["id"]
    else:
        # Manejar posible error 500 del servidor de la API
        if response.status_code == 500:
            pytest.fail(
                f"La API devolvió un error 500 (Internal Server Error) al intentar crear un usuario de "
                f"prueba para eliminar. "
                f"Esto indica un posible fallo interno en el servidor de la API. "
                f"Cuerpo de la respuesta: {response.text}"
            )
        # Para otros errores, fallar con el mensaje original
        pytest.fail(
            f"Falló la creación del usuario de prueba para eliminar. Status: "
            f"{response.status_code}, Body: {response.text}")


def test_delete_user_as_admin():
    """
    TC-API-09: Eliminar usuario.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un usuario de prueba para eliminar
    user_id_to_delete = create_test_user_for_deletion(token)

    # 3. Hacer la solicitud DELETE a /users/{user_id}
    response = requests.delete(f"{BASE_URL}/users/{user_id_to_delete}", headers=headers)

    # 4. Verificar el código de estado.
    # DELETE exitoso debe devolver 204 No Content
    # Manejar el posible error 500 del servidor de la API
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar eliminar el usuario. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 204, (
        f"Error al eliminar usuario. "
        f"Esperaba 204 (No Content), obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    print(f"✅ Usuario eliminado exitosamente. ID: {user_id_to_delete}")

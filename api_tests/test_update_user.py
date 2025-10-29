import requests
import pytest
import time
from jsonschema import validate
from conftest import BASE_URL

"""
Caso de prueba: TC-API-08: Actualizar usuario (PUT /users/{user_id})
Objetivo: Verificar que un usuario autenticado como admin pueda actualizar la información de otro usuario.
"""
@pytest.mark.TC_API_08
@pytest.mark.medium
@pytest.mark.users
@pytest.mark.positive
@pytest.mark.api
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


def create_test_user(admin_token):
    """
    Crea un usuario de prueba para actualizarlo.
    Asegura trabajar con un usuario controlado y evita modificar datos reales.
    Devuelve un diccionario con 'id', 'email' y 'password' del usuario creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    timestamp = int(time.time())
    user_data = {
        "email": f"update_test_{timestamp}@test.com",
        "password": "InitialPass123!",
        "full_name": f"Initial Name {timestamp}",
        "role": "passenger"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=headers)

    if response.status_code == 201:
        # Éxito: Devolver un diccionario con todos los datos necesarios
        response_data = response.json()
        return {
            "id": response_data["id"],
            "email": user_data["email"],
            "password": user_data["password"]
        }
    else:
        # Manejar posible error 500 del servidor de la API
        if response.status_code == 500:
            pytest.fail(
                f"La API devolvió un error 500 (Internal Server Error) al intentar crear un usuario. "
                f"Esto indica un posible fallo interno en el servidor de la API. "
                f"Cuerpo de la respuesta: {response.text}"
            )
        # Para otros errores, fallar con el mensaje original
        pytest.fail(f"Falló la creación del usuario de prueba. Status: {response.status_code}, Body: {response.text}")


def test_update_user_as_admin():
    """
    TC-API-08: Actualizar usuario.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un usuario de prueba para actualizar
    user_data_for_update = create_test_user(token)
    user_id_to_update = user_data_for_update["id"]
    original_email = user_data_for_update["email"]
    original_password = user_data_for_update["password"]

    # 3. Preparar datos para la actualización.
    # Actualizar solo el nombre completo.
    updated_data = {
        "email": original_email,  # Reenviar el email original
        "password": original_password,  # Reenviar la contraseña original
        "full_name": "Nombre Actualizado"
        # Se omite 'role' para evitar posibles restricciones o comportamientos no reflejados
    }

    # 4. Hacer la solicitud PUT a /users/{user_id}
    response = requests.put(f"{BASE_URL}/users/{user_id_to_update}", json=updated_data, headers=headers)

    # 5. Verificar el código de estado.
    # Manejar posible error 500 del servidor de la API
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar actualizar el usuario. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de actualización debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al actualizar usuario. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura de la respuesta
    updated_user = response.json()
    assert isinstance(updated_user, dict), f"Se esperaba un diccionario, se obtuvo {type(updated_user)}"

    # Verificar que los campos se hayan actualizado correctamente
    assert updated_user["id"] == user_id_to_update, "El ID del usuario no coincide"
    assert updated_user["full_name"] == updated_data["full_name"], (
        f"El nombre no se actualizó. "
        f"Esperado: {updated_data['full_name']}, Obtenido: {updated_user['full_name']}"
    )
    # Se asume que el email no cambia en esta actualización, por lo que debe seguir presente
    assert "email" in updated_user and updated_user[
        "email"] == original_email, "El email no es correcto en la respuesta"

    print(
        f"✅ Usuario actualizado exitosamente. ID: {updated_user['id']}, Nuevo nombre: "
        f"{updated_user['full_name']}")

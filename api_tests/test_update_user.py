import requests
import pytest
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
def test_update_user_as_admin(admin_token, new_user_data):
    """
    TC-API-08: Actualizar usuario.
    Este test recibe 'admin_token' y 'new_user_data' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Crear un usuario de prueba para actualizar usando los datos del fixture
    response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=headers)

    # Manejar errores comunes durante la creación
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear un usuario. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 201, (
        f"Falló la creación del usuario de prueba. Status: {response.status_code}, Body: {response.text}"
    )

    response_data = response.json()
    user_id_to_update = response_data["id"]
    original_email = new_user_data["email"]
    original_password = new_user_data["password"]

    # 2. Preparar datos para la actualización.
    # Actualizar solo el nombre completo.
    updated_data = {
        "email": original_email,  # Reenviar el email original
        "password": original_password,  # Reenviar la contraseña original
        "full_name": "Nombre Actualizado"
        # Se omite 'role' para evitar posibles restricciones o comportamientos no reflejados
    }

    # 3. Hacer la solicitud PUT a /users/{user_id}
    response = requests.put(f"{BASE_URL}/users/{user_id_to_update}", json=updated_data, headers=headers)

    # 4. Verificar el código de estado.
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

    # 5. Validar la estructura de la respuesta
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

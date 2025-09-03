import requests
import pytest
import time
from jsonschema import validate
from conftest import BASE_URL


def test_delete_user_as_admin(admin_token, user_id_to_delete):
    """
    TC-API-09: Eliminar usuario.
    Este test recibe 'admin_token' y 'test_user_id_to_delete' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_id_to_delete = user_id_to_delete

    # 3. Hacer la solicitud DELETE a /users/{user_id}
    response = requests.delete(f"{BASE_URL}/users/{user_id_to_delete}", headers=headers)

    # 4. Verificar el código de estado.
    # Un DELETE exitoso debe devolver 204 No Content
    # Manejar el posible error 500 del servidor de la API
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar eliminar el usuario. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 204, (
        f"Error al eliminar usuario. "
        f"Esperaba 204 (No Content), obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    print(f"✅ Usuario eliminado exitosamente. ID: {user_id_to_delete}")

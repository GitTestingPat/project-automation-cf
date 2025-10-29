import requests
import pytest
from jsonschema import validate
from conftest import BASE_URL

"""
Caso de prueba: TC-API-05: Listar todos los usuarios (autenticado)
Objetivo: Verificar que un usuario autenticado pueda obtener la lista de todos los usuarios.
"""
@pytest.mark.TC_API_05
@pytest.mark.high
@pytest.mark.users
@pytest.mark.positive
@pytest.mark.api
def get_admin_token():
    """
    Obtiene un token JWT para un usuario administrador.
    """
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    # Comprueba login exitoso para continuar
    assert response.status_code == 200, (f"Falló el login de admin. Status: {response.status_code}, "
                                         f"Body: {response.text}")

    token_data = response.json()
    return token_data["access_token"]


def test_list_users_as_admin():
    """
    TC-API-05: Listar todos los usuarios (autenticado).
    """
    # 1. Obtener token de autenticación como admin
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Hacer la solicitud GET a /users/
    response = requests.get(f"{BASE_URL}/users/", headers=headers)

    # Comprobar si el servidor devuelve error 500, es un fallo interno de la API de prueba.
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar listar usuarios. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba"
            f"Cuerpo de la respuesta: {response.text}"
        )

    # 3. Verificar que la respuesta sea exitosa (200 OK)
    assert response.status_code == 200, f"Esperaba 200, obtuvo {response.status_code}. Cuerpo: {response.text}"

    # 4. Verificar que la respuesta sea una lista de usuarios
    users = response.json()
    assert isinstance(users, list), f"Se esperaba una lista de usuarios, se obtuvo {type(users)}"

    # 5. Verificar que cada usuario en la lista tenga la estructura básica esperada
    if users:
        first_user = users[0]
        assert "id" in first_user, "Falta 'id' en el objeto de usuario"
        assert "email" in first_user, "Falta 'email' en el objeto de usuario"
        assert "@" in first_user["email"], "El 'email' no tiene un formato válido"
        assert "full_name" in first_user, "Falta 'full_name' en el objeto de usuario"
        # verificar que el campo 'role' es válido
        if "role" in first_user:
            assert first_user["role"] in ["passenger", "admin"], f"Rol inválido: {first_user['role']}"

    print(f"✅ Listados {len(users)} usuarios correctamente como administrador.")

import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-07: Obtener mi perfil (GET /users/me/)
Objetivo: Verificar que un usuario autenticado pueda obtener su propia información de perfil.
"""
@pytest.mark.TC_API_07
@pytest.mark.medium
@pytest.mark.users
@pytest.mark.positive
@pytest.mark.api
def test_get_my_profile(admin_token):
    """
    TC-API-07: Obtener mi perfil.
    Este test recibe 'admin_token' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Hacer la solicitud GET a /users/me/
    response = requests.get(f"{BASE_URL}/users/me/", headers=headers)

    # 2. Verificar que la respuesta sea exitosa (200 OK)
    # Manejar el posible error 500 del servidor de la API
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

    # 3. Validar la estructura del perfil del usuario (esquema UserOut)
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


@pytest.mark.TC_API_07b
@pytest.mark.medium
@pytest.mark.users
@pytest.mark.positive
@pytest.mark.api
def test_get_my_profile_as_regular_user(auth_token):
    """
    TC-API-07b: Obtener mi perfil como usuario regular.
    ✅ COBERTURA: Usa fixture auth_token (conftest líneas 78-134) que creaba 0 consumers.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(f"{BASE_URL}/users/me/", headers=headers)

    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al obtener perfil con auth_token. "
            f"Cuerpo: {response.text}"
        )

    assert response.status_code == 200, (
        f"Error al obtener perfil con auth_token. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    user_profile = response.json()
    assert "id" in user_profile, "Falta 'id' en el perfil"
    assert "email" in user_profile, "Falta 'email' en el perfil"
    assert "@" in user_profile["email"], "Email sin formato válido"
    print(f"✅ Perfil obtenido con auth_token. Email: {user_profile['email']}")

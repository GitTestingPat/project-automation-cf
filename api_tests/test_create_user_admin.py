import requests
import pytest
import time
from conftest import BASE_URL
from jsonschema import validate

"""
TC-API-06: Crear usuario como admin.
Objetivo: crear un nuevo usuario con permisos de administrador.              
"""

def test_create_user_as_admin(admin_token, new_user_data):
    """
    TC-API-06: Crear usuario como admin.
    Este test recibe 'admin_token' y 'new_user_data' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Preparar datos para el nuevo usuario que ya vienen del fixture 'new_user_data'
    # El fixture 'new_user_data' genera un email único.
    new_user_email = new_user_data["email"] # El email es único gracias al fixture

    # 3. Hacer la solicitud POST a /users/
    response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=headers)

    # 4. Verificar el código de estado.
    # Manejar el fallo interno de la API.
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

    # 5. Verificar la estructura del usuario creado (esquema UserOut)
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
    # Validar que el campo 'role' sea válido
    if "role" in created_user:
         assert created_user["role"] in ["passenger", "admin"], f"Rol inválido: {created_user['role']}"

    print(f"✅ Usuario creado exitosamente como admin. ID: {created_user['id']}, Email: {created_user['email']}")

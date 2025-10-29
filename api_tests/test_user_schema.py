import requests
import pytest
from jsonschema import validate, ValidationError
from schemas.user_schema import USER_SCHEMA
from conftest import BASE_URL
import time

"""
Prueba TC-API-01: Registrar usuario válido
Objetivo: Comprobar que se pueda registrar en el sistema un usuario con datos válidos.
Módulo: Auth
Prioridad: Alta
Tipo: Positivo
"""
@pytest.mark.TC_API_01
@pytest.mark.high
@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.api
def test_signup_returns_valid_schema():
    """
    TC-API-01: Registrar usuario válido

    Precondiciones:
    - La API debe estar disponible
    - El email debe ser único

    Pasos:
    1. Generar datos de usuario con email único
    2. Enviar POST a /auth/signup
    3. Validar código de respuesta 201
    4. Validar que el esquema de respuesta sea correcto

    Resultado esperado:
    - Código: 201 Created
    - Respuesta cumple con USER_SCHEMA
    """
    # Generar un email único con timestamp
    timestamp = int(time.time())
    email = f"test_user_{timestamp}@example.com"

    # Datos para registrarse
    user_data = {
        "email": email,
        "password": "123456",
        "full_name": "Test User"
    }

    # Usar el endpoint correcto para registro público
    response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)

    # Manejar error 500 del servidor de la API
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar registrar un usuario. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # Verificar que el registro sea exitoso
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Body: {response.text}"

    # Obtener el usuario creado
    user = response.json()

    # Validar que el esquema sea correcto
    try:
        validate(instance=user, schema=USER_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"El esquema no es válido: {e.message}")
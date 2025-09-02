import requests
import pytest
from jsonschema import validate, ValidationError
from schemas.user_schema import USER_SCHEMA
import time

'''
Prueba TC-API-01 Registrar usuario válido
'''

BASE_URL = "https://cf-automation-airline-api.onrender.com"

def test_signup_returns_valid_schema():
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

    # Manejar posible error 500 del servidor de la API
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
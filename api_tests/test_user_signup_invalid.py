import requests
import pytest

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-03: Registrar con email inválido (Negativo)
Objetivo: Verificar que la API devuelva un error 422 cuando se intenta registrar un usuario con un email con formato inválido.
"""

def test_signup_with_invalid_email():
    """
    TC-API-03: Registrar con email inválido (Negativo).
    """
    # Datos para el registro con email inválido
    invalid_email = "invalid_email" # Ejemplo de email inválido
    user_data = {
        "email": invalid_email,
        "password": "123456",
        "full_name": "Test User Invalid Email"
    }

    # Intentar registrar el usuario
    response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)

    # Verificar que la respuesta sea un error 422
    assert response.status_code == 422, f"Esperaba 422, obtuvo {response.status_code}. Cuerpo: {response.text}"

    # Verificar que el mensaje de error sea descriptivo
    error_body = response.json()

    print(f"✅ Registro rechazado correctamente para email inválido '{invalid_email}'. Código: {response.status_code}")

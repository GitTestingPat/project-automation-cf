import requests
import pytest

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-04: Iniciar sesión con credenciales válidas.
Objetivo: Verificar que un usuario registrado pueda iniciar sesión correctamente y recibir un token JWT.
"""

def test_login_with_valid_credentials():
    """
    TC-API-04: Iniciar sesión con credenciales válidas.
    """
    # Credenciales de un usuario que se sabe existe y es válido.
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }

    # Realizar la solicitud POST para iniciar sesión
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    # Verificar que la respuesta sea exitosa (200 OK)
    assert response.status_code == 200, (
        f"Error al iniciar sesión. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # Parsear la respuesta JSON
    response_data = response.json()

    # Verificar que la respuesta contenga los campos esperados para un token
    assert "access_token" in response_data, (
        "La respuesta no contiene 'access_token'. "
        f"Campos recibidos: {list(response_data.keys())}"
    )
    assert "token_type" in response_data, (
        "La respuesta no contiene 'token_type'. "
        f"Campos recibidos: {list(response_data.keys())}"
    )

    # Verificar que el tipo de token sea 'bearer' (o el valor por defecto esperado)
    assert response_data["token_type"] == "bearer", (
        f"Tipo de token inesperado. Esperado: 'bearer', Obtenido: '{response_data['token_type']}'"
    )

    # Verificar que el access_token no esté vacío
    assert response_data["access_token"], "El 'access_token' devuelto está vacío."

    print(f"✅ Login exitoso. Token type: {response_data['token_type']}, Token length: "
          f"{len(response_data['access_token'])} characters.")

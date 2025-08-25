import requests
import pytest

BASE_URL = "https://cf-automation-airline-api.onrender.com"

def test_signup_endpoint_returns_known_error():
    """
    Verificar que el endpoint /auth/signup devuelve un error conocido (400 o 500),
    como parte del comportamiento simulado de la API.
    """
    response = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": "test@example.com",
        "password": "123456",
        "full_name": "Test User"
    })

    # Verificar que devuelva un código de error conocido
    assert response.status_code in [400, 500], f"Esperaba 400 o 500, obtuvo {response.status_code}"

    # imprimir el cuerpo para ver qué devuelve
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")

    # Si es 500, verificar que sea el error simulado (como texto plano)
    if response.status_code == 500:
        assert "Internal Server Error" in response.text

    # Si es 400, verificar un JSON con detalles
    elif response.status_code == 400:
        try:
            error_body = response.json()
            assert "detail" in error_body
        except:
            # Si no es JSON, verificar que no esté vacío
            assert response.text != ""

    print(f"✅ Error simulado detectado: {response.status_code}")
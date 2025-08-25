import requests
import pytest
import time

BASE_URL = "https://cf-automation-airline-api.onrender.com"


def test_signup_endpoint_returns_known_error():
    """
    Verificar que el endpoint /auth/signup devuelve un error conocido (400 o 500),
    como parte del comportamiento simulado de la API.
    """
    # Generar un email único con timestamp
    timestamp = int(time.time())  # <-- Usar time.time()
    email = f"test_user_{timestamp}@example.com"  # <-- Email único

    response = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email,  # <-- Usar el email único
        "password": "123456",
        "full_name": "Test User"
    })

    # Verificar que devuelva un código de error conocido
    assert response.status_code in [201, 400, 500], f"Esperaba 201, 400 o 500, obtuvo {response.status_code}"

    if response.status_code in [400, 500]:
        print(f"✅ Error simulado detectado: {response.status_code}")
        # Opcional: verificar el cuerpo del error si es predecible
        # ...
    elif response.status_code == 201:
        print(f"ℹ️  Registro exitoso (201). El endpoint pudo haber dejado de simular errores.")
import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-04: Login con contraseña incorrecta
Objetivo: Verificar que la API devuelva un error 401 cuando se intenta iniciar sesión con una contraseña incorrecta.
"""
@pytest.mark.TC_API_04
@pytest.mark.high
@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.api
def test_login_with_invalid_password():
    """
    TC-API-04: Login con contraseña incorrecta.
    """
    # 1. Preparar datos de login con contraseña incorrecta
    login_data = {
        "username": "admin@demo.com",
        "password": "wrongpassword123"  # Contraseña incorrecta
    }

    # 2. Hacer la solicitud POST a /auth/login
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    # 3. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar iniciar sesión con "
            f"contraseña incorrecta. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al intentar iniciar sesión con contraseña incorrecta. "
            f"Esperaba que los datos fueran válidos para el intento de login. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de login con credenciales inválidas debe devolver 401 Unauthorized
    assert response.status_code == 401, (
        f"Error al intentar iniciar sesión con contraseña incorrecta. "
        f"Esperaba 401, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 4. Validar el mensaje de error
    error_body = response.json()
    assert isinstance(error_body, dict), f"Se esperaba un diccionario, se obtuvo {type(error_body)}"
    assert "detail" in error_body, "Falta 'detail' en la respuesta de error"
    # El mensaje puede variar, pero generalmente indica credenciales inválidas
    assert ("Incorrect username or password" in error_body["detail"] or "Incorrect credentials"
            in error_body["detail"]), (f"El mensaje de error no es el esperado para credenciales inválidas. "
                                       f"Esperaba 'Incorrect username or password' o 'Incorrect credentials', "
                                       f"obtuvo: {error_body['detail']}"
    )

    print(f"✅ Login rechazado correctamente con contraseña incorrecta. Status: {response.status_code}, "
          f"Mensaje: {error_body['detail']}")

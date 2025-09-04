import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-30: Probar error 400 (GET /glitch-examples/client-error)
Objetivo: Verificar que la API devuelva correctamente un error 400 Bad Request cuando se accede al endpoint.
"""

def test_client_error_endpoint_returns_400():
    """
    TC-API-30: Probar error 400.
    """
    # 1. Hacer la solicitud GET al endpoint que devuelve error 400
    response = requests.get(f"{BASE_URL}/glitch-examples/client-error")

    # 2. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar acceder al endpoint 'client-error'. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 200:
        pytest.fail(
            f"La API devolvió 200 OK al intentar acceder al endpoint 'client-error'. "
            f"Esto indica que el endpoint no simuló el error 400 como se esperaba. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de error 400 debe devolver 400 Bad Request
    assert response.status_code == 400, (
        f"Error al probar endpoint 'client-error'. "
        f"Esperaba 400, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # Verificar que el cuerpo de la respuesta sea un JSON válido
    try:
        error_body = response.json()
    except ValueError:
        pytest.fail(
            f"El cuerpo de la respuesta del error 400 no es un JSON válido. "
            f"Esto indica un posible fallo en la serialización de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # Verificar que el cuerpo tenga la estructura de un error estándar
    assert isinstance(error_body, dict), f"Se esperaba un diccionario, se obtuvo {type(error_body)}"

    # Verificar que contenga una clave 'detail' con un mensaje de error
    assert "detail" in error_body, (
        f"Falta la clave 'detail' en la respuesta del error 400. "
        f"Cuerpo de la respuesta: {response.text}"
    )
    assert isinstance(error_body["detail"], str), (
        f"El valor de 'detail' en la respuesta del error 400 debe ser un string. "
        f"Obtenido: {type(error_body['detail'])}"
    )
    # Verificar que el mensaje no debe estar vacío (puede variar)
    assert error_body["detail"], (
        f"El mensaje de error en 'detail' no debe estar vacío. "
        f"Obtenido: '{error_body['detail']}'"
    )

    print(f"✅ Endpoint 'client-error' devolvió 400 Bad Request correctamente. "
          f"Mensaje: {error_body['detail']}")

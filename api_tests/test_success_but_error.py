import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-29: Probar endpoint que simula éxito con error
Objetivo: Verificar que el cliente pueda manejar correctamente una respuesta donde el código de estado es 200 OK,
          pero el cuerpo contiene un mensaje de error.
Nota: Esta prueba interactúa con un endpoint especial de la API que simula este comportamiento.
"""
@pytest.mark.TC_API_29
@pytest.mark.low
@pytest.mark.negative
@pytest.mark.api
def test_success_but_error_endpoint():
    """
    TC-API-29: Probar endpoint que simula éxito con error.
    """
    # 1. Hacer la solicitud GET al endpoint que simula éxito con error
    response = requests.get(f"{BASE_URL}/glitch-examples/success-but-error")

    # 2. Verificar el código de estado.
    # Este endpoint está diseñado para devolver 200 OK
    assert response.status_code == 200, (
        f"Error al llamar al endpoint 'success-but-error'. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 3. Parsear el cuerpo de la respuesta como JSON
    try:
        response_data = response.json()
    except ValueError as e:
        pytest.fail(
            f"El cuerpo de la respuesta no es un JSON válido. "
            f"Esto indica un posible fallo en la serialización de la API. "
            f"Error: {e}. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # 4. Verificar que el cuerpo contenga un mensaje que indique un error a pesar del 200 OK
    assert isinstance(response_data, dict), (
        f"Se esperaba un diccionario en el cuerpo de la respuesta, se obtuvo {type(response_data)}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # Verificar que el cuerpo contenga alguna clave que indique un problema
    # Puede ser 'error', 'detail', 'message', etc.
    error_indicators = ["error", "detail", "message"]
    found_indicator = None
    for key in error_indicators:
        if key in response_data:
            found_indicator = key
            break

    assert found_indicator is not None, (
        f"El cuerpo de la respuesta no contiene ninguna clave indicadora de error. "
        f"Se esperaba una de {error_indicators}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # Verificar que el contenido de la clave indicadora exista.
    print(
        f"✅ Endpoint 'success-but-error' devolvió 200 OK con indicador de error: "
        f"'{found_indicator}' = '{response_data[found_indicator]}'")


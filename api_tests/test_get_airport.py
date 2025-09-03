import requests
import pytest
import time
import random
import string
from conftest import BASE_URL

"""
Caso de prueba: TC-API-12: Obtener aeropuerto (GET /airports/{iata_code})
Objetivo: Verificar que se pueda obtener la información de un aeropuerto específico mediante su código IATA.
"""

def test_get_airport_by_iata_code(airport_iata_code):
    """
    TC-API-15: Obtener aeropuerto.
    """
    iata_code_to_get = airport_iata_code # El código IATA ya viene del fixture

    # 2. Hacer la solicitud GET a /airports/{iata_code}
    response = requests.get(f"{BASE_URL}/airports/{iata_code_to_get}")

    # 3. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar obtener el aeropuerto. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación en el código IATA al obtener aeropuerto. "
            f"Esto podría indicar un problema con el formato del código '{iata_code_to_get}'. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar obtener el aeropuerto '{iata_code_to_get}'. "
            f"Esto indica que el aeropuerto no fue encontrado, a pesar de haber sido creado. "
            f"Puede ser un problema de consistencia en la API o un retraso en la indexación. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de obtención exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al obtener aeropuerto. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 4. Validar la estructura y datos de la respuesta (esquema AirportOut)
    airport_data = response.json()
    assert isinstance(airport_data, dict), f"Se esperaba un diccionario, se obtuvo {type(airport_data)}"

    # Verificar que los campos devueltos sean correctos
    assert "iata_code" in airport_data, "Falta 'iata_code' en la respuesta"
    assert airport_data["iata_code"] == iata_code_to_get, (
        f"El código IATA obtenido no coincide. "
        f"Esperado: {iata_code_to_get}, Obtenido: {airport_data['iata_code']}"
    )
    assert "city" in airport_data, "Falta 'city' en la respuesta"
    assert "country" in airport_data, "Falta 'country' en la respuesta"

    print(f"✅ Aeropuerto obtenido exitosamente. IATA: {airport_data['iata_code']}, Ciudad: "
          f"{airport_data.get('city', 'N/A')}")


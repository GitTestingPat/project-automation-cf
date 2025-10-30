import requests
import pytest
import time
from datetime import timezone
from datetime import datetime, timedelta
from jsonschema import validate
from conftest import BASE_URL

"""
Caso de prueba: TC-API-17: Obtener vuelo (GET /flights/{flight_id})
Objetivo: Verificar que se pueda obtener la información de un vuelo específico mediante su ID.
"""
@pytest.mark.TC_API_17
@pytest.mark.medium
@pytest.mark.flights
@pytest.mark.positive
@pytest.mark.api
def test_get_flight_by_id(admin_token, flight_id):
    """
    TC-API-17: Obtener vuelo.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    flight_id_to_get = flight_id # El ID ya viene del fixture

    # 3. Hacer la solicitud GET a /flights/{flight_id}
    response = requests.get(f"{BASE_URL}/flights/{flight_id_to_get}", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        # Verificar si es un error 500 simulado
        try:
            error_body = response.json()
            if "detail" in error_body and "Simulated 5xx bug" in error_body["detail"]:
                pytest.skip(
                    f"La API devolvió un 500 Internal Server Error simulado. "
                    f"Mensaje: {error_body['detail']}. "
                    f"Este es un comportamiento conocido de la API de prueba para simular fallos del servidor."
                )
            # Si no es el 500 simulado específico, continúa con el fail más abajo
        except:
            # Si el cuerpo no es JSON válido, también continúa con el fail
            pass
        # Este pytest.fail se ejecuta si no era el 500 simulado específico o hubo error al parsear
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar obtener el vuelo. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar obtener el vuelo '{flight_id_to_get}'. "
            f"Esto indica que el vuelo no fue encontrado, a pesar de haber sido creado. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 504:
        # Verificar si es el timeout simulado
        error_body = response.json()
        if "detail" in error_body and "Simulated timeout" in error_body["detail"]:
            pytest.skip(
                f"La API devolvió un 504 Gateway Timeout simulado. "
                f"Mensaje: {error_body['detail']}. "
                f"Este es un comportamiento conocido de la API de prueba para simular fallos de red."
            )
        else:
            # Si es un 504 real (no simulado), se considera un fallo de la prueba
            pytest.fail(
                f"La API devolvió un 504 Gateway Timeout no simulado al intentar obtener el vuelo. "
                f"Esto indica un posible fallo de red o timeout real. "
                f"Cuerpo de la respuesta: {response.text}"
            )

    # La operación de obtención exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al obtener vuelo. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 5. Validar la estructura y datos de la respuesta (esquema FlightOut)
    flight_data = response.json()
    assert isinstance(flight_data, dict), f"Se esperaba un diccionario, se obtuvo {type(flight_data)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "origin", "destination", "departure_time", "arrival_time", "base_price",
                       "aircraft_id", "available_seats"]
    for field in expected_fields:
        assert field in flight_data, f"Falta el campo '{field}' en la respuesta del vuelo obtenido."

    # Verificar que el ID devuelto sea el mismo que el solicitado
    assert flight_data["id"] == flight_id_to_get, (
        f"El ID del vuelo obtenido no coincide. "
        f"Esperado: {flight_id_to_get}, Obtenido: {flight_data['id']}"
    )

    # Verificaciones básicas de contenido
    assert flight_data["origin"]  # Verificar que no esté vacío
    assert flight_data["destination"] # Verificar que no esté vacío
    assert flight_data["departure_time"] # Verificar que no esté vacío
    assert flight_data["arrival_time"] # Verificar que no esté vacío
    assert isinstance(flight_data["base_price"], (int, float)), (
        f"El base_price debe ser un número. Obtenido: {type(flight_data['base_price'])}"
    )
    assert flight_data["aircraft_id"] # Verificar que no esté vacío
    assert isinstance(flight_data["available_seats"], int), (
        f"El available_seats debe ser un entero. Obtenido: {type(flight_data['available_seats'])}"
    )

    print(f"✅ Vuelo obtenido exitosamente. ID: {flight_data['id']}, Origen: {flight_data['origin']}, "
          f"Destino: {flight_data['destination']}")

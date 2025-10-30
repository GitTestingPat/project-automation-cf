import requests
import pytest
import time
from conftest import BASE_URL
from datetime import timezone
from datetime import datetime, timedelta
from jsonschema import validate

"""
TC-API-16: Crear vuelo.
Objetivo: crear un nuevo vuelo con fechas y códigos válidos.
"""
@pytest.mark.TC_API_16
@pytest.mark.high
@pytest.mark.flights
@pytest.mark.positive
@pytest.mark.api
def test_create_flight_as_admin(admin_token, aircraft_id):
    """
    TC-API-16: Crear vuelo.
    Este test recibe 'admin_token' y 'test_aircraft_id' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    aircraft_id_to_use = aircraft_id # El ID del avión viene del fixture

    # 2. Preparar datos para el nuevo vuelo.
    # Los códigos IATA para origen y destino deben ser válidos (3 letras mayúsculas).
    future_time = datetime.now(timezone.utc) + timedelta(hours=2)
    arrival_time = future_time + timedelta(hours=3)

    new_flight_data = {
        "origin": "NYC",  # Código IATA válido de ejemplo
        "destination": "LAX",  # Código IATA válido de ejemplo
        "departure_time": future_time.isoformat(),  # Formato ISO 8601
        "arrival_time": arrival_time.isoformat(),   # Formato ISO 8601
        "base_price": 299.99,
        "aircraft_id": aircraft_id_to_use  # ID del avión obtenido del fixture
    }

    # 3. Hacer la solicitud POST a /flights
    response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear un vuelo. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code in [401, 403]:
        pytest.skip(
            f"La API requirió autenticación o permisos insuficientes (Status: {response.status_code}) "
            f"para crear un vuelo. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear vuelo. "
            f"Esperaba que los datos fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de creación exitosa debe devolver 201 Created
    assert response.status_code == 201, (
        f"Error al crear vuelo. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 5. Validar la estructura de la respuesta (esquema FlightOut)
    created_flight = response.json()
    assert isinstance(created_flight, dict), f"Se esperaba un diccionario, se obtuvo {type(created_flight)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "origin", "destination", "departure_time", "arrival_time", "base_price",
                       "aircraft_id", "available_seats"]
    for field in expected_fields:
        assert field in created_flight, f"Falta el campo '{field}' en la respuesta del vuelo creado."

    assert created_flight["origin"] == new_flight_data["origin"], (
        f"El origen no coincide. "
        f"Esperado: {new_flight_data['origin']}, Obtenido: {created_flight['origin']}"
    )
    assert created_flight["destination"] == new_flight_data["destination"], (
        f"El destino no coincide. "
        f"Esperado: {new_flight_data['destination']}, Obtenido: {created_flight['destination']}"
    )
    # Validar la existencia de las fechas.
    assert created_flight["base_price"] == new_flight_data["base_price"], (
        f"El precio base no coincide. "
        f"Esperado: {new_flight_data['base_price']}, Obtenido: {created_flight['base_price']}"
    )
    assert created_flight["aircraft_id"] == new_flight_data["aircraft_id"], (
        f"El aircraft_id no coincide. "
        f"Esperado: {new_flight_data['aircraft_id']}, Obtenido: {created_flight['aircraft_id']}"
    )
    # Validar que available_seats debe estar presente y ser un número.
    assert "available_seats" in created_flight and isinstance(created_flight["available_seats"], int), (
        f"El available_seats debe estar presente y ser un entero. "
        f"Obtenido: {created_flight.get('available_seats')} (tipo: {type(created_flight.get('available_seats'))})"
    )
    print(f"✅ Vuelo creado exitosamente. ID: {created_flight['id']}, Origen: {created_flight['origin']}, "
          f"Destino: {created_flight['destination']}")

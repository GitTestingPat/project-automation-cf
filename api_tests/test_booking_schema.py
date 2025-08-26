import requests
import pytest
from jsonschema import validate
from schemas.booking_schema import BOOKING_SCHEMA

BASE_URL = "https://cf-automation-airline-api.onrender.com"


def test_create_booking_returns_valid_schema(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Buscar vuelos
    response = requests.get(
        f"{BASE_URL}/flights/",
        params={"origin": "MEX", "destination": "CUN"}
    )
    if response.status_code != 200:
        print("Respuesta al buscar vuelos:", response.text)
    assert response.status_code == 200, f"Error al buscar vuelos: {response.status_code}"

    flights = response.json()

    # Verificar que la respuesta sea una lista (aunque esté vacía)
    assert isinstance(flights, list), f"Se esperaba una lista de vuelos, se obtuvo: {type(flights)}"

    # Verificar que haya al menos un vuelo
    # Si no hay vuelos, la prueba fallará aquí, lo cual es correcto si se requiere uno.
    assert len(flights) > 0, f"No hay vuelos disponibles para reservar. La API devolvió: {flights}"

    # Verificar que el primer elemento tenga la clave 'id'
    first_flight = flights[0]
    assert isinstance(first_flight, dict), f"El primer elemento no es un diccionario: {type(first_flight)}"
    assert "id" in first_flight, f"El primer vuelo no tiene clave 'id': {first_flight.keys()}"

    # Tomar el primer vuelo
    flight_id = first_flight["id"]

    # Crear una reserva
    booking_data = {
        "flight_id": flight_id,
        "passengers": [
            {
                "full_name": "Ana López",
                "passport": "MX987654"
            }
        ]
    }

    booking_response = requests.post(
        f"{BASE_URL}/bookings",
        json=booking_data,
        headers=headers
    )

    assert booking_response.status_code == 201, f"Error al crear reserva: {booking_response.text}"
    booking = booking_response.json()

    # Validar esquema
    try:
        validate(instance=booking, schema=BOOKING_SCHEMA)
    except Exception as e:
        pytest.fail(f"Error de validación de esquema: {e}")
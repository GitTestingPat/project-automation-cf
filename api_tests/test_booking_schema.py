import requests
import pytest
from jsonschema import validate
from schemas.booking_schema import BOOKING_SCHEMA

BASE_URL = "https://cf-automation-airline-api.onrender.com"


def test_create_booking_returns_valid_schema(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Buscar vuelos
    response = requests.get(f"{BASE_URL}/flights/search/")

    assert response.status_code == 200, f"Error al buscar vuelos: {response.status_code}"

    flights = response.json()

    # Verificar que haya al menos un vuelo
    assert len(flights) > 0, "No hay vuelos disponibles para reservar"

    # Tomar el primer vuelo
    flight_id = flights[0]["id"]

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
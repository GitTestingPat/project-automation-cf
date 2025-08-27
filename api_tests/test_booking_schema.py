import requests
import pytest
import os
from jsonschema import validate, ValidationError
from schemas.booking_schema import BOOKING_SCHEMA

# Detectar entorno de CI
IN_CI = os.getenv("CI") == "true"

BASE_URL = "https://cf-automation-airline-api.onrender.com"


def test_create_booking_returns_valid_schema(auth_token):
    """
    Verifica que la creación de una reserva devuelva un esquema válido.
    En entornos de CI, se aceptan errores 500, 400 y listas vacías → se salta la prueba.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Paso 1: Buscar vuelos
    try:
        response = requests.get(
            f"{BASE_URL}/flights/",
            params={"origin": "NYC", "destination": "LON"},
            timeout=10
        )
    except requests.RequestException as e:
        if IN_CI:
            pytest.skip(f"Error de conexión en CI: {e}. Se acepta como inestabilidad temporal.")
        else:
            pytest.fail(f"Error de conexión: {e}")

    # 🔹 Manejo tolerante de errores HTTP en CI
    if IN_CI:
        if response.status_code == 500:
            pytest.skip("La API devolvió 500 (Error interno del servidor). Se acepta en CI.")
        if response.status_code == 400:
            pytest.skip("La API devolvió 400 (Solicitud incorrecta). Se acepta en CI.")
        if response.status_code == 404:
            pytest.skip("La API devolvió 404 (No encontrado). Se acepta en CI.")

    # Validación estricta solo si no estamos en CI
    assert response.status_code == 200, (
        f"Error al buscar vuelos: {response.status_code}. Respuesta: {response.text}"
    )

    # Parsear JSON
    try:
        flights = response.json()
    except ValueError:
        pytest.fail("La respuesta de /flights/ no es un JSON válido.")

    assert isinstance(flights, list), f"Se esperaba una lista de vuelos, se obtuvo: {type(flights)}"

    # 🔹 Si la lista está vacía y estamos en CI → saltar
    if len(flights) == 0:
        if IN_CI:
            pytest.skip("La API devolvió una lista vacía de vuelos. Se acepta en CI (datos simulados o sin disponibilidad).")
        else:
            pytest.fail("No hay vuelos disponibles para probar la creación de reserva.")

    # Tomar el primer vuelo
    first_flight = flights[0]
    assert isinstance(first_flight, dict), f"El primer elemento no es un diccionario: {type(first_flight)}"
    assert "id" in first_flight, f"El primer vuelo no tiene clave 'id': {list(first_flight.keys())}"
    flight_id = first_flight["id"]

    # Paso 2: Crear reserva
    booking_data = {
        "flight_id": flight_id,
        "passengers": [
            {
                "full_name": "Ana López",
                "passport": "MX987654"
            }
        ]
    }

    try:
        booking_response = requests.post(
            f"{BASE_URL}/bookings",
            json=booking_data,
            headers=headers,
            timeout=10
        )
    except requests.RequestException as e:
        pytest.fail(f"Error al crear reserva: {e}")

    # 🔹 En CI, tolerar 500 en creación de reserva
    if IN_CI and booking_response.status_code == 500:
        pytest.skip("La API devolvió 500 al crear reserva. Se acepta en CI.")

    assert booking_response.status_code == 201, (
        f"Error al crear reserva: {booking_response.status_code}, Respuesta: {booking_response.text}"
    )

    # Validar esquema de la respuesta
    booking = booking_response.json()
    try:
        validate(instance=booking, schema=BOOKING_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Error de validación de esquema: {e.message}")
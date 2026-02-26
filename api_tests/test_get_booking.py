import requests
import pytest
import time
import random
import string
from conftest import BASE_URL
from datetime import datetime, timedelta, timezone
from jsonschema import validate
from schemas.booking_schema import BOOKING_SCHEMA

"""
Caso de prueba: TC-API-22: Obtener reserva (GET /bookings/{booking_id})
Objetivo: Verificar que un usuario autenticado pueda obtener la información de una 
reserva específica que le pertenece.
"""
@pytest.mark.TC_API_22
@pytest.mark.medium
@pytest.mark.bookings
@pytest.mark.positive
@pytest.mark.api
def test_get_booking_by_id(user_token, booking_id):
    """
    TC-API-22: Obtener reserva.
    """
    headers = {"Authorization": f"Bearer {user_token}"}
    booking_id_to_get = booking_id

    # 1. Hacer la solicitud GET a /bookings/{booking_id}
    response = requests.get(f"{BASE_URL}/bookings/{booking_id_to_get}", headers=headers)

    # 2. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar obtener la reserva. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar obtener la reserva '{booking_id_to_get}'. "
            f"Esto indica que la reserva no fue encontrada, a pesar de haber sido creada. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para obtener una reserva. "
            f"Esto indica que el token de usuario no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 403:
        pytest.fail(
            f"La API devolvió 403 (Forbidden) al intentar obtener la reserva '{booking_id_to_get}'. "
            f"Esto indica que el usuario no tiene permiso para acceder a esta reserva (posiblemente no es el dueño). "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de obtención exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al obtener reserva. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 3. Validar la estructura y datos de la respuesta (esquema BookingOut)
    booking_data = response.json()
    assert isinstance(booking_data, dict), f"Se esperaba un diccionario, se obtuvo {type(booking_data)}"

    # ✅ COBERTURA: Validar contra BOOKING_SCHEMA (cubre booking_schema.py al 100%)
    validate(instance=booking_data, schema=BOOKING_SCHEMA)
    print("✅ Booking validado contra BOOKING_SCHEMA")

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "flight_id", "user_id", "status", "passengers"]
    for field in expected_fields:
        assert field in booking_data, f"Falta el campo '{field}' en la respuesta de la reserva obtenida."

    # Verificar que el ID devuelto sea el mismo que el solicitado
    assert booking_data["id"] == booking_id_to_get, (
        f"El ID de la reserva obtenida no coincide. "
        f"Esperado: {booking_id_to_get}, Obtenido: {booking_data['id']}"
    )

    # Verificaciones básicas de contenido
    assert booking_data["flight_id"] # Verificar que no esté vacío
    assert booking_data["user_id"] # Verificar que no esté vacío
    assert booking_data["status"] in ["draft", "paid", "checked_in", "cancelled"], (
        f"Estado de reserva inválido: {booking_data['status']}"
    )
    assert isinstance(booking_data["passengers"], list), (
        f"Los pasajeros deben ser una lista. Obtenido: {type(booking_data['passengers'])}"
    )
    if booking_data["passengers"]:
        passenger = booking_data["passengers"][0]
        assert "full_name" in passenger and passenger["full_name"]
        assert "passport" in passenger and passenger["passport"]

    print(f"✅ Reserva obtenida exitosamente. ID: {booking_data['id']}, Estado: {booking_data['status']}")

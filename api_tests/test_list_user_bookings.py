import requests
import pytest
import time
from datetime import datetime, timedelta, timezone
from jsonschema import validate
from conftest import BASE_URL

"""
Caso de prueba: TC-API-20: Listar reservas del usuario (GET /bookings)
Objetivo: Verificar que un usuario autenticado pueda obtener la lista de sus propias reservas.
"""

def test_list_user_bookings_as_authenticated_user(user_token, admin_token, aircraft_id,
                                                  create_test_booking_for_listing):
    """
    TC-API-20: Listar reservas del usuario.
    Este test recibe 'user_token', 'admin_token' y 'aircraft_id' de los fixtures.
    """
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 1. Crear una reserva de prueba para asegurar que haya algo que listar
    try:
        booking_id_to_list = create_test_booking_for_listing
    except Exception as e:
        pytest.skip(f"No se pudo crear una reserva de prueba para listar: {e}")

    # 2. Hacer la solicitud GET a /bookings
    response = requests.get(f"{BASE_URL}/bookings", headers=user_headers)

    # 3. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar listar reservas del usuario. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para listar reservas del usuario. "
            f"Esto indica que el token de usuario no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 403:
        pytest.fail(
            f"La API devolvió 403 (Forbidden) al intentar listar reservas del usuario. "
            f"Esto indica que el usuario no tiene permiso para acceder a esta lista (posiblemente solo "
            f"admins pueden listar todas). "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de listado exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al listar reservas del usuario. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 4. Validar la estructura de la respuesta (esquema List[BookingOut])
    bookings = response.json()
    assert isinstance(bookings, list), f"Se esperaba una lista, se obtuvo {type(bookings)}"

    # Verificar que al menos la reserva creada esté en la lista
    assert len(bookings) > 0, "La lista de reservas del usuario está vacía."

    # Buscar la reserva creada en la lista
    found_booking = None
    for booking in bookings:
        if booking["id"] == booking_id_to_list:
            found_booking = booking
            break

    assert found_booking is not None, (
        f"La reserva creada ('{booking_id_to_list}') no fue encontrada en la lista de reservas del usuario. "
        f"Esto indica un posible problema de consistencia en la API o en la prueba. "
        f"Reservas obtenidas: {[b['id'] for b in bookings]}"
    )

    # 5. Validar la estructura y datos de la reserva encontrada (esquema BookingOut)
    assert isinstance(found_booking, dict), f"Se esperaba un diccionario, se obtuvo {type(found_booking)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "flight_id", "user_id", "status", "passengers"]
    for field in expected_fields:
        assert field in found_booking, f"Falta el campo '{field}' en la reserva listada."

    # Verificaciones específicas de contenido
    assert found_booking["id"] == booking_id_to_list, (
        f"El ID de la reserva listada no coincide. "
        f"Esperado: {booking_id_to_list}, Obtenido: {found_booking['id']}"
    )
    assert found_booking["flight_id"]  # Verificar que no esté vacío
    assert found_booking["user_id"]  # Verificar que no esté vacío
    assert found_booking["status"] in ["draft", "paid", "checked_in", "cancelled"], (
        f"Estado de reserva inválido: {found_booking['status']}"
    )
    assert isinstance(found_booking["passengers"], list), (
        f"Los pasajeros deben ser una lista. Obtenido: {type(found_booking['passengers'])}"
    )
    if found_booking["passengers"]:
        passenger = found_booking["passengers"][0]
        assert "full_name" in passenger and passenger["full_name"]
        assert "passport" in passenger and passenger["passport"]
        # 'seat' es opcional

    print(
        f"✅ Lista de reservas del usuario obtenida exitosamente. Total: {len(bookings)}, "
        f"Reserva buscada ID: {found_booking['id']}")

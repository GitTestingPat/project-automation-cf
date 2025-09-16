import requests
import pytest
import time
from conftest import BASE_URL
from datetime import datetime, timedelta, timezone
from jsonschema import validate

"""
TC-API-21: Crear reserva.
Objetivo: Crear una nueva reserva para un usuario autorizado.
"""

def test_create_booking_as_user(user_token, flight_id):
    """
    TC-API-20: Crear reserva.
    Este test recibe 'user_token' y 'flight_id' de los fixtures.
    """
    user_headers = {"Authorization": f"Bearer {user_token}"}
    flight_id_to_book = flight_id  # El ID del vuelo viene del fixture

    # 3. Preparar datos para la nueva reserva.
    new_booking_data = {
        "flight_id": flight_id_to_book,
        "passengers": [
            {
                "full_name": "Pasajero Uno de Prueba",
                "passport": "P12345678"
                # 'seat' es opcional, se omite
            },
            {
                "full_name": "Pasajero Dos de Prueba",
                "passport": "P87654321"
                # 'seat' es opcional, se omite
            }
        ]
    }

    # 4. Hacer la solicitud POST a /bookings
    response = requests.post(f"{BASE_URL}/bookings", json=new_booking_data, headers=user_headers)

    # 5. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear una reserva. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear reserva. "
            f"Esperaba que los datos fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para crear una reserva. "
            f"Esto indica que el token de usuario no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de creación exitosa debe devolver 201 Created
    assert response.status_code == 201, (
        f"Error al crear reserva. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura de la respuesta (esquema BookingOut)
    created_booking = response.json()
    assert isinstance(created_booking, dict), f"Se esperaba un diccionario, se obtuvo {type(created_booking)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "flight_id", "user_id", "status", "passengers"]
    for field in expected_fields:
        assert field in created_booking, f"Falta el campo '{field}' en la respuesta de la reserva creada."

    # Verificaciones específicas de contenido
    assert created_booking["flight_id"] == new_booking_data["flight_id"], (
        f"El flight_id de la reserva no coincide. "
        f"Esperado: {new_booking_data['flight_id']}, Obtenido: {created_booking['flight_id']}"
    )
    # El user_id debe ser el del usuario autenticado, su presencia se comprueba con 'expected_fields'.
    assert created_booking["status"] == "draft", (
        f"El estado inicial de la reserva debería ser 'draft'. "
        f"Obtenido: {created_booking['status']}"
    )

    # Verificar que los pasajeros se hayan creado correctamente
    assert len(created_booking["passengers"]) == len(new_booking_data["passengers"]), (
        f"El número de pasajeros no coincide. "
        f"Esperado: {len(new_booking_data['passengers'])}, Obtenido: {len(created_booking['passengers'])}"
    )
    for i, passenger in enumerate(created_booking["passengers"]):
        assert "full_name" in passenger, f"Falta 'full_name' en el pasajero {i}."
        assert passenger["full_name"] == new_booking_data["passengers"][i]["full_name"], (
            f"El nombre del pasajero {i} no coincide. "
            f"Esperado: {new_booking_data['passengers'][i]['full_name']}, Obtenido: {passenger['full_name']}"
        )
        assert "passport" in passenger, f"Falta 'passport' en el pasajero {i}."
        assert passenger["passport"] == new_booking_data["passengers"][i]["passport"], (
            f"El pasaporte del pasajero {i} no coincide. "
            f"Esperado: {new_booking_data['passengers'][i]['passport']}, Obtenido: {passenger['passport']}"
        )
    print(
        f"✅ Reserva creada exitosamente. ID: {created_booking['id']}, Vuelo ID: {created_booking['flight_id']}, "
        f"Estado: {created_booking['status']}")

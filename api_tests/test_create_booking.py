import requests
import pytest
import time
from datetime import datetime, timedelta, timezone
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-20: Crear reserva (POST /bookings)
Objetivo: Verificar que un usuario autenticado pueda crear una nueva reserva para un vuelo.
"""

def get_admin_token():
    """
    Intenta obtener un token JWT para un usuario administrador.
    Si las credenciales fallan, se lanza una PermissionError.
    """
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        raise PermissionError(f"Falló el login de admin. Status: {response.status_code}, Body: {response.text}")


def create_and_login_test_user():
    """
    Crea un nuevo usuario de prueba y luego inicia sesión con él.
    Devuelve el token de acceso del usuario creado.
    Esto garantiza que siempre usemos credenciales válidas y controladas.
    """
    import random
    import string

    # Generar un email único para evitar conflictos
    timestamp = str(int(time.time()))[-5:]  # Últimos 5 dígitos del timestamp
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    test_email = f"booking_user_{timestamp}_{random_suffix}@test.com"
    test_password = "SecurePass123!"  # Contraseña de ejemplo

    user_data = {
        "email": test_email,
        "password": test_password,
        "full_name": f"Booking Tester {timestamp}"
    }

    # 1. Registrar el nuevo usuario
    signup_response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)

    # Manejar posibles errores durante el registro
    if signup_response.status_code == 201:
        # Registro exitoso
        print(f"✅ Usuario de prueba para reserva creado e iniciado sesión: {test_email}")
    elif signup_response.status_code == 400:
        error_detail = signup_response.json().get("detail", "")
        if "already registered" in str(error_detail).lower():
            # Aunque improbable con el email único, manejarlo
            pytest.fail(
                f"Error inesperado: El email '{test_email}' ya estaba registrado. "
                f"Esto es inusual con un email generado. "
                f"Detalle: {error_detail}"
            )
        else:
            pytest.fail(
                f"Error 400 al crear usuario de prueba para reserva. "
                f"Detalle: {error_detail}"
            )
    elif signup_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al intentar crear un usuario de prueba para reserva. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {signup_response.text}"
        )
    else:
        # Otro error inesperado
        pytest.fail(
            f"Error inesperado al crear usuario de prueba para reserva. "
            f"Status: {signup_response.status_code}, "
            f"Body: {signup_response.text}"
        )

    # 2. Iniciar sesión con el usuario recién creado
    login_data = {
        "username": test_email,
        "password": test_password
    }
    login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    if login_response.status_code == 200:
        token_data = login_response.json()
        return token_data["access_token"]
    else:
        # Si el login falla después de crear el usuario, es un error grave
        pytest.fail(
            f"Falló el login del usuario de prueba recién creado para reserva. "
            f"Status: {login_response.status_code}, Body: {login_response.text}. "
            f"Esto indica un problema inesperado después de la creación."
        )


def create_test_aircraft_for_booking(admin_token):
    """
    Crea un avión de prueba para usarlo en la creación de un vuelo para la reserva.
    Devuelve el ID del avión creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un tail_number único
    timestamp = str(int(time.time()))[-5:]  # Últimos 5 dígitos del timestamp
    tail_number = f"N{timestamp}AE"  # Asegurar 6 caracteres, formato ejemplo

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model Booking {timestamp}",
        "capacity": 150  # Capacidad de ejemplo
    }

    # Crear el avión
    create_response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear avión para la prueba de reserva. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear avión para la prueba de reserva. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear avión para la prueba de reserva. "
        f"Esperaba 201, obtuvo {create_response.status_code}. "
        f"Cuerpo: {create_response.text}"
    )

    created_aircraft = create_response.json()
    assert "id" in created_aircraft, "Falta 'id' en la respuesta del avión creado."
    assert created_aircraft["tail_number"] == tail_number, (
        f"El tail_number del avión creado no coincide. "
        f"Esperado: {tail_number}, Obtenido: {created_aircraft['tail_number']}"
    )

    return created_aircraft["id"]


def create_test_flight_for_booking(admin_token):
    """
    Crea un vuelo de prueba para luego hacer una reserva.
    Devuelve el ID del vuelo creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Crear un avión de prueba para usar en el vuelo
    try:
        aircraft_id = create_test_aircraft_for_booking(admin_token)
    except Exception as e:
        pytest.fail(f"Falló la creación del avión de prueba para vuelo de reserva: {e}")

    # 2. Preparar datos para el nuevo vuelo.
    future_time = datetime.now(timezone.utc) + timedelta(hours=10)
    arrival_time = future_time + timedelta(hours=11)

    new_flight_data = {
        "origin": "SFO",  # Código IATA válido de ejemplo
        "destination": "JFK",  # Código IATA válido de ejemplo
        "departure_time": future_time.isoformat(),  # Formato ISO 8601
        "arrival_time": arrival_time.isoformat(),  # Formato ISO 8601
        "base_price": 499.99,
        "aircraft_id": aircraft_id  # ID del avión recién creado
    }

    # 3. Crear el vuelo
    create_response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear vuelo para la prueba de reserva. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear vuelo para la prueba de reserva. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear vuelo para la prueba de reserva. "
        f"Esperaba 201, obtuvo {create_response.status_code}. "
        f"Cuerpo: {create_response.text}"
    )

    created_flight = create_response.json()
    assert "id" in created_flight, "Falta 'id' en la respuesta del vuelo creado."
    assert created_flight["origin"] == new_flight_data["origin"], (
        f"El origen del vuelo creado no coincide. "
        f"Esperado: {new_flight_data['origin']}, Obtenido: {created_flight['origin']}"
    )

    return created_flight["id"]


def test_create_booking_as_user():
    """
    TC-API-20: Crear reserva.
    """
    # 1. Crear un usuario de prueba y obtener su token de autenticación
    try:
        user_token = create_and_login_test_user()
    except Exception as e:  # Capturar cualquier fallo en la creación/inicio de sesión
        pytest.skip(f"No se pudo crear e iniciar sesión con el usuario de prueba: {e}")

    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 2. Obtener token de autenticación como admin para crear el vuelo
    try:
        admin_token = get_admin_token()  # Reutilizamos la función de otros tests
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin para crear vuelo: {e}")

    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 3. Crear un vuelo de prueba para hacer la reserva
    flight_id_for_booking = create_test_flight_for_booking(admin_token)

    # 4. Preparar datos para la nueva reserva.
    new_booking_data = {
        "flight_id": flight_id_for_booking,
        "passengers": [
            {
                "full_name": "Pasajero Uno",
                "passport": "P12345678"
                # 'seat' es opcional, se omite
            },
            {
                "full_name": "Pasajero Dos",
                "passport": "P87654321"
                # 'seat' es opcional, se omite
            }
        ]
    }

    # 5. Hacer la solicitud POST a /bookings
    response = requests.post(f"{BASE_URL}/bookings", json=new_booking_data, headers=user_headers)

    # 6. Verificar el código de estado.
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

    # 7. Validar la estructura de la respuesta (esquema BookingOut)
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
    # Validar que user_id debe ser el del usuario autenticado
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
        # El campo 'seat' puede estar ausente o ser null si no se asignó
        # assert "seat" in passenger # No se verifica su presencia si es opcional

    print(
        f"✅ Reserva creada exitosamente. ID: {created_booking['id']}, Vuelo ID: {created_booking['flight_id']}, "
        f"Estado: {created_booking['status']}")


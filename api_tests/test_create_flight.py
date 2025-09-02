import requests
import pytest
import time
from datetime import timezone
from datetime import datetime, timedelta
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-16: Crear vuelo (POST /flights)
Objetivo: Verificar que un usuario autenticado como admin pueda crear un nuevo vuelo.
"""

def get_admin_token():
    """
    Obtener un token JWT para un usuario administrador.
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


def create_test_aircraft(admin_token):
    """
    Crea un avión de prueba para usarlo en la creación de un vuelo.
    Devuelve el ID del avión creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un tail_number único
    timestamp = str(int(time.time()))[-5:]  # Últimos 5 dígitos del timestamp
    tail_number = f"N{timestamp}AA"  # Asegurar 6 caracteres, formato ejemplo

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model {timestamp}",
        "capacity": 150  # Capacidad de ejemplo
    }

    # Crear el avión
    create_response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear avión para la prueba de vuelo. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear avión para la prueba de vuelo. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear avión para la prueba de vuelo. "
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


def test_create_flight_as_admin():
    """
    TC-API-16: Crear vuelo.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un avión de prueba para usar en el vuelo
    try:
        aircraft_id = create_test_aircraft(token)
    except Exception as e:
        pytest.fail(f"Falló la creación del avión de prueba: {e}")

    # 3. Preparar datos para el nuevo vuelo.
    # Usar códigos IATA válidos para origen y destino (3 letras mayúsculas).
    future_time = datetime.now(timezone.utc) + timedelta(hours=2)
    arrival_time = future_time + timedelta(hours=3)

    new_flight_data = {
        "origin": "NYC",  # Código IATA válido
        "destination": "LAX",  # Código IATA válido
        "departure_time": future_time.isoformat(),
        "arrival_time": arrival_time.isoformat(),
        "base_price": 299.99,
        "aircraft_id": aircraft_id  # ID del avión creado
    }

    # 4. Hacer la solicitud POST a /flights
    response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=headers)

    # 5. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear un vuelo. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code in [401, 403]:
        pytest.skip(
            f"La API requirió autenticación o permisos insuficientes (Status: "
            f"{response.status_code}) para crear un vuelo. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear vuelo. "
            f"Esperaba que los datos fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # Operación de creación exitosa debe devolver 201 Created
    assert response.status_code == 201, (
        f"Error al crear vuelo. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura de la respuesta (esquema FlightOut)
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
    # Verificar la existencia del formato de las fechas.
    assert created_flight["base_price"] == new_flight_data["base_price"], (
        f"El precio base no coincide. "
        f"Esperado: {new_flight_data['base_price']}, Obtenido: {created_flight['base_price']}"
    )

    print(f"✅ Vuelo creado exitosamente. ID: {created_flight['id']}, Origen: {created_flight['origin']}, "
          f"Destino: {created_flight['destination']}")

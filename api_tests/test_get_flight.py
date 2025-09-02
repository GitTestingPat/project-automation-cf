import requests
import pytest
import time
from datetime import timezone
from datetime import datetime, timedelta
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-17: Obtener vuelo (GET /flights/{flight_id})
Objetivo: Verificar que se pueda obtener la información de un vuelo específico mediante su ID.
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


def create_test_aircraft_for_flight(admin_token):
    """
    Crea un avión de prueba para usarlo en la creación de un vuelo.
    Devuelve el ID del avión creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un tail_number único
    timestamp = str(int(time.time()))[-5:]  # Últimos 5 dígitos del timestamp
    tail_number = f"N{timestamp}AB"  # Asegurar 6 caracteres, formato ejemplo

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model Get {timestamp}",
        "capacity": 180  # Capacidad de ejemplo
    }

    # Crear el avión
    create_response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear avión para la prueba de obtención de vuelo. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear avión para la prueba de obtención de vuelo. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear avión para la prueba de obtención de vuelo. "
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


def create_test_flight_for_retrieval(admin_token):
    """
    Crea un vuelo de prueba para luego obtenerlo.
    Devuelve el ID del vuelo creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Crear un avión de prueba para usar en el vuelo
    try:
        aircraft_id = create_test_aircraft_for_flight(admin_token)
    except Exception as e:
        pytest.fail(f"Falló la creación del avión de prueba para vuelo: {e}")

    # 2. Preparar datos para el nuevo vuelo.
    future_time = datetime.now(timezone.utc) + timedelta(hours=4)
    arrival_time = future_time + timedelta(hours=5)

    new_flight_data = {
        "origin": "MEX",  # Código IATA válido
        "destination": "BCN",  # Código IATA válido
        "departure_time": future_time.isoformat() + "Z",  # Formato ISO 8601
        "arrival_time": arrival_time.isoformat() + "Z",  # Formato ISO 8601
        "base_price": 599.99,
        "aircraft_id": aircraft_id  # ID del avión creado
    }

    # 3. Crear el vuelo
    create_response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear vuelo para la prueba de obtención. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear vuelo para la prueba de obtención. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear vuelo para la prueba de obtención. "
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


def test_get_flight_by_id():
    """
    TC-API-17: Obtener vuelo.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un vuelo de prueba
    flight_id_to_get = create_test_flight_for_retrieval(token)

    # 3. Hacer la solicitud GET a /flights/{flight_id}
    response = requests.get(f"{BASE_URL}/flights/{flight_id_to_get}", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
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
    expected_fields = ["id", "origin", "destination", "departure_time", "arrival_time", "base_price", "aircraft_id",
                       "available_seats"]
    for field in expected_fields:
        assert field in flight_data, f"Falta el campo '{field}' en la respuesta del vuelo obtenido."

    # Verificar que el ID devuelto sea el mismo que el solicitado
    assert flight_data["id"] == flight_id_to_get, (
        f"El ID del vuelo obtenido no coincide. "
        f"Esperado: {flight_id_to_get}, Obtenido: {flight_data['id']}"
    )

    # Validaciones básicas de contenido
    assert flight_data["origin"]  # Valida que no esté vacío
    assert flight_data["destination"]  # Valida que no esté vacío
    assert flight_data["departure_time"]  # Valida que no esté vacío
    assert flight_data["arrival_time"]  # Valida que no esté vacío
    assert isinstance(flight_data["base_price"], (int, float)), (
        f"El base_price debe ser un número. Obtenido: {type(flight_data['base_price'])}"
    )
    assert flight_data["aircraft_id"]  # Valida que no esté vacío
    assert isinstance(flight_data["available_seats"], int), (
        f"El available_seats debe ser un entero. Obtenido: {type(flight_data['available_seats'])}"
    )

    print(
        f"✅ Vuelo obtenido exitosamente. ID: {flight_data['id']}, Origen: {flight_data['origin']}, "
        f"Destino: {flight_data['destination']}")

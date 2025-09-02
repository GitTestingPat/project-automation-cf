import requests
import pytest
import time
from datetime import datetime, timedelta, timezone
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-19: Eliminar vuelo (DELETE /flights/{flight_id})
Objetivo: Verificar que un usuario autenticado como admin pueda eliminar un vuelo específico.
Nota: Esta prueba requiere un usuario con permisos de administrador.
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


def create_test_aircraft_for_deletion(admin_token):
    """
    Crea un avión de prueba para usarlo en la creación de un vuelo que luego se eliminará.
    Devuelve el ID del avión creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un tail_number único
    timestamp = str(int(time.time()))[-5:]  # Últimos 5 dígitos del timestamp
    tail_number = f"N{timestamp}AD"  # Asegurar 6 caracteres, formato ejemplo

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model Delete {timestamp}",
        "capacity": 180  # Capacidad de ejemplo
    }

    # Crear el avión
    create_response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear avión para la prueba de eliminación de vuelo. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear avión para la prueba de eliminación de vuelo. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear avión para la prueba de eliminación de vuelo. "
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


def create_test_flight_for_deletion(admin_token):
    """
    Crea un vuelo de prueba para luego eliminarlo.
    Devuelve el ID del vuelo creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Crear un avión de prueba para usar en el vuelo
    try:
        aircraft_id = create_test_aircraft_for_deletion(admin_token)
    except Exception as e:
        pytest.fail(f"Falló la creación del avión de prueba para vuelo: {e}")

    # 2. Preparar datos para el nuevo vuelo.
    future_time = datetime.now(timezone.utc) + timedelta(hours=8)
    arrival_time = future_time + timedelta(hours=9)

    new_flight_data = {
        "origin": "FRA",  # Código IATA válido de ejemplo
        "destination": "MAD",  # Código IATA válido de ejemplo
        "departure_time": future_time.isoformat(),  # Formato ISO 8601
        "arrival_time": arrival_time.isoformat(),  # Formato ISO 8601
        "base_price": 350.50,
        "aircraft_id": aircraft_id  # ID del avión recién creado
    }

    # 3. Crear el vuelo
    create_response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear vuelo para la prueba de eliminación. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear vuelo para la prueba de eliminación. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear vuelo para la prueba de eliminación. "
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


def test_delete_flight_as_admin():
    """
    TC-API-19: Eliminar vuelo.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un vuelo de prueba para eliminar
    flight_id_to_delete = create_test_flight_for_deletion(token)

    # 3. Hacer la solicitud DELETE a /flights/{flight_id}
    response = requests.delete(f"{BASE_URL}/flights/{flight_id_to_delete}", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar eliminar el vuelo. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar eliminar el vuelo '{flight_id_to_delete}'. "
            f"Esto indica que el vuelo no fue encontrado, a pesar de haber sido creado. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de eliminación exitosa debería devolver 204 No Content
    assert response.status_code == 204, (
        f"Error al eliminar vuelo. "
        f"Esperaba 204 (No Content), obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    print(f"✅ Vuelo eliminado exitosamente. ID: {flight_id_to_delete}")

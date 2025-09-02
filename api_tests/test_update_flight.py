import requests
import pytest
import time
from datetime import datetime, timedelta
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-18: Actualizar vuelo (PUT /flights/{flight_id})
Objetivo: Verificar que un usuario autenticado como admin pueda actualizar la información de un vuelo específico.
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


def create_test_aircraft_for_update(admin_token):
    """
    Crea un avión de prueba para usarlo en la creación y posterior actualización de un vuelo.
    Devuelve el ID del avión creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un tail_number único
    timestamp = str(int(time.time()))[-5:]  # Últimos 5 dígitos del timestamp
    tail_number = f"N{timestamp}AC"  # Asegurar 6 caracteres, formato ejemplo

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model Update {timestamp}",
        "capacity": 200  # Capacidad de ejemplo
    }

    # Crear el avión
    create_response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear avión para la prueba de actualización de vuelo. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear avión para la prueba de actualización de vuelo. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear avión para la prueba de actualización de vuelo. "
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


def create_test_flight_for_update(admin_token):
    """
    Crea un vuelo de prueba para luego actualizarlo.
    Devuelve el ID del vuelo creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Crear un avión de prueba para usar en el vuelo
    try:
        aircraft_id = create_test_aircraft_for_update(admin_token)
    except Exception as e:
        pytest.fail(f"Falló la creación del avión de prueba para vuelo: {e}")

    # 2. Preparar datos para el nuevo vuelo.
    future_time = datetime.utcnow() + timedelta(hours=6)
    arrival_time = future_time + timedelta(hours=7)

    new_flight_data = {
        "origin": "LHR",  # Código IATA válido
        "destination": "CDG",  # Código IATA válido
        "departure_time": future_time.isoformat() + "Z",  # Formato ISO 8601
        "arrival_time": arrival_time.isoformat() + "Z",  # Formato ISO 8601
        "base_price": 450.00,
        "aircraft_id": aircraft_id  # ID del avión creado
    }

    # 3. Crear el vuelo
    create_response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear vuelo para la prueba de actualización. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear vuelo para la prueba de actualización. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear vuelo para la prueba de actualización. "
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


def test_update_flight_as_admin():
    """
    TC-API-18: Actualizar vuelo.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un vuelo de prueba para actualizar
    flight_id_to_update = create_test_flight_for_update(token)

    # 3. Preparar datos actualizados.
    updated_departure_time = datetime.utcnow() + timedelta(hours=8)
    updated_arrival_time = updated_departure_time + timedelta(hours=9)

    updated_flight_data = {
        "origin": "DXB",  # Nuevo origen
        "destination": "SIN",  # Nuevo destino
        "departure_time": updated_departure_time.isoformat() + "Z",  # Nueva hora de salida
        "arrival_time": updated_arrival_time.isoformat() + "Z",  # Nueva hora de llegada
        "base_price": 550.75,  # Nuevo precio base
        "aircraft_id": "aircraft-id-placeholder"  # Placeholder, será reemplazado
    }

    # 4. Hacer la solicitud PUT a /flights/{flight_id}
    get_response = requests.get(f"{BASE_URL}/flights/{flight_id_to_update}", headers=headers)
    assert get_response.status_code == 200, (
        f"Error al obtener el vuelo original para actualizar. "
        f"Esperaba 200, obtuvo {get_response.status_code}. "
        f"Cuerpo: {get_response.text}"
    )
    original_flight_data = get_response.json()
    # Actualizar aircraft_id en los datos a enviar
    updated_flight_data["aircraft_id"] = original_flight_data["aircraft_id"]

    response = requests.put(f"{BASE_URL}/flights/{flight_id_to_update}", json=updated_flight_data, headers=headers)

    # 5. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar actualizar el vuelo. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al actualizar vuelo. "
            f"Esperaba que los datos actualizados fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar actualizar el vuelo '{flight_id_to_update}'. "
            f"Esto indica que el vuelo no fue encontrado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de actualización exitosa debería devolver 200 OK
    assert response.status_code == 200, (
        f"Error al actualizar vuelo. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura y datos de la respuesta
    updated_flight = response.json()
    assert isinstance(updated_flight, dict), f"Se esperaba un diccionario, se obtuvo {type(updated_flight)}"

    # Verificar que los campos se hayan actualizado correctamente
    assert updated_flight["id"] == flight_id_to_update, (
        f"El ID del vuelo no debería cambiar. "
        f"Esperado: {flight_id_to_update}, Obtenido: {updated_flight['id']}"
    )
    assert updated_flight["origin"] == updated_flight_data["origin"], (
        f"El origen no se actualizó. "
        f"Esperado: {updated_flight_data['origin']}, Obtenido: {updated_flight['origin']}"
    )
    assert updated_flight["destination"] == updated_flight_data["destination"], (
        f"El destino no se actualizó. "
        f"Esperado: {updated_flight_data['destination']}, Obtenido: {updated_flight['destination']}"
    )
    assert updated_flight["base_price"] == updated_flight_data["base_price"], (
        f"El precio base no se actualizó. "
        f"Esperado: {updated_flight_data['base_price']}, Obtenido: {updated_flight['base_price']}"
    )
    # Verificar que aircraft_id siga siendo el mismo
    assert updated_flight["aircraft_id"] == updated_flight_data["aircraft_id"], (
        f"El aircraft_id no debería haber cambiado. "
        f"Esperado: {updated_flight_data['aircraft_id']}, Obtenido: {updated_flight['aircraft_id']}"
    )
    # Confirmar que las fechas también se hayan actualizado
    assert updated_flight["departure_time"] == updated_flight_data["departure_time"], (
        f"La hora de salida no se actualizó. "
        f"Esperado: {updated_flight_data['departure_time']}, Obtenido: {updated_flight['departure_time']}"
    )
    assert updated_flight["arrival_time"] == updated_flight_data["arrival_time"], (
        f"La hora de llegada no se actualizó. "
        f"Esperado: {updated_flight_data['arrival_time']}, Obtenido: {updated_flight['arrival_time']}"
    )

    print(
        f"✅ Vuelo actualizado exitosamente. ID: {updated_flight['id']}, Nuevo Origen: {updated_flight['origin']}, "
        f"Nuevo Destino: {updated_flight['destination']}")

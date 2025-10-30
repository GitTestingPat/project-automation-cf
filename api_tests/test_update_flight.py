import requests
import pytest
import time
from conftest import BASE_URL
from datetime import datetime, timedelta, timezone
from jsonschema import validate

"""
TC-API-18: Actualizar vuelo.
Objetivo: Confirmar que el un vuelo creado siga existiendo con los mismos datos enviados.
"""
@pytest.mark.TC_API_18
@pytest.mark.medium
@pytest.mark.flights
@pytest.mark.positive
@pytest.mark.api
def test_update_flight_as_admin(admin_token, flight_id):
    """
    TC-API-18: Actualizar vuelo.
    Este test ahora recibe 'admin_token' y 'flight_id' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    flight_id_to_update = flight_id # El ID del vuelo viene del fixture

    # 3. Preparar datos actualizados.
    updated_departure_time = datetime.now(timezone.utc) + timedelta(hours=8)
    updated_arrival_time = updated_departure_time + timedelta(hours=9)

    updated_flight_data = {
        "origin": "DXB",  # Nuevo origen
        "destination": "SIN",  # Nuevo destino
        "departure_time": updated_departure_time.isoformat(),  # Nueva hora de salida
        "arrival_time": updated_arrival_time.isoformat(),   # Nueva hora de llegada
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
    # Actualizar el aircraft_id en los datos a enviar
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

    # La operación de actualización exitosa debe devolver 200 OK
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
    # Confirmar que las fechas también se hayan actualizado.
    try:
        expected_departure_dt = datetime.fromisoformat(updated_flight_data["departure_time"].replace("Z",
                                                                                                     "+00:00"))
        actual_departure_dt = datetime.fromisoformat(updated_flight["departure_time"].replace("Z", "+00:00"))
        assert actual_departure_dt == expected_departure_dt, (
            f"La hora de salida no se actualizó correctamente. "
            f"Esperado (parseado): {expected_departure_dt}, Obtenido (parseado): {actual_departure_dt}"
        )
    except ValueError as e:
        pytest.fail(
            f"Error al parsear las fechas para comparar la hora de salida. "
            f"Esperado: {updated_flight_data['departure_time']}, Obtenido: {updated_flight['departure_time']}. "
            f"Error: {e}"
        )

    try:
        expected_arrival_dt = datetime.fromisoformat(updated_flight_data["arrival_time"].replace("Z",
                                                                                                 "+00:00"))
        actual_arrival_dt = datetime.fromisoformat(updated_flight["arrival_time"].replace("Z", "+00:00"))
        assert actual_arrival_dt == expected_arrival_dt, (
            f"La hora de llegada no se actualizó correctamente. "
            f"Esperado (parseado): {expected_arrival_dt}, Obtenido (parseado): {actual_arrival_dt}"
        )
    except ValueError as e:
        pytest.fail(
            f"Error al parsear las fechas para comparar la hora de llegada. "
            f"Esperado: {updated_flight_data['arrival_time']}, Obtenido: {updated_flight['arrival_time']}. "
            f"Error: {e}"
        )

    print(f"✅ Vuelo actualizado exitosamente. ID: {updated_flight['id']}, Nuevo Origen: "
          f"{updated_flight['origin']}, Nuevo Destino: {updated_flight['destination']}")

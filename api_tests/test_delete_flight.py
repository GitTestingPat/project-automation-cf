import requests
import pytest
import time
from conftest import BASE_URL
from datetime import datetime, timedelta, timezone
from jsonschema import validate

"""
TC-API-19: Eliminar vuelo.
Objetivo: Eliminar un vuelo previamente creado usando datos válidos.
"""
@pytest.mark.TC_API_19
@pytest.mark.low
@pytest.mark.flights
@pytest.mark.positive
@pytest.mark.api
def test_delete_flight_as_admin(admin_token, flight_id):
    """
    TC-API-19: Eliminar vuelo.
    Este test recibe 'admin_token' y 'flight_id' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    flight_id_to_delete = flight_id # El ID del vuelo ya viene del fixture

    # 3. Hacer la solicitud DELETE a /flights/{flight_id}
    response = requests.delete(f"{BASE_URL}/flights/{flight_id_to_delete}", headers=headers)

    # 4. Verificar el código de estado.
    # Un DELETE exitoso debe devolver 204 No Content.
    # Manejar el posible error 500 del servidor de la API.
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

    # La operación de eliminación exitosa debe devolver 204 No Content
    assert response.status_code == 204, (
        f"Error al eliminar vuelo. "
        f"Esperaba 204 (No Content), obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    print(f"✅ Vuelo eliminado exitosamente. ID: {flight_id_to_delete}")


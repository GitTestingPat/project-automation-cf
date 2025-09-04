import requests
import pytest
import time
import random
import string
from conftest import BASE_URL
from jsonschema import validate

"""
TC-API-14: Eliminar aeropuerto.
Objetivo: Eliminar un aeropuerto ya creado usando datos válidos.
"""

def test_delete_airport_as_admin(admin_token, airport_iata_code):
    """
    TC-API-14: Eliminar aeropuerto.
    Este test recibe 'admin_token' y 'airport_iata_code' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    iata_code_to_delete = airport_iata_code

    # 3. Hacer la solicitud DELETE a /airports/{iata_code}
    response = requests.delete(f"{BASE_URL}/airports/{iata_code_to_delete}", headers=headers)

    # 4. Verificar el código de estado.
    # Un DELETE exitoso debe devolver 204 No Content.
    # Manejar el posible error 500 del servidor de la API.
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar eliminar el aeropuerto. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar eliminar el aeropuerto '{iata_code_to_delete}'. "
            f"Esto indica que el aeropuerto no fue encontrado, a pesar de haber sido creado. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de eliminación exitosa debe devolver 204 No Content
    assert response.status_code == 204, (
        f"Error al eliminar aeropuerto. "
        f"Esperaba 204 (No Content), obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    print(f"✅ Aeropuerto eliminado exitosamente. IATA: {iata_code_to_delete}")


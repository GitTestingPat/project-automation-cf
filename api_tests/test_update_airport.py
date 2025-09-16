import requests
import pytest
import time
import random
import string
from conftest import BASE_URL
from jsonschema import validate

"""
Caso de prueba: TC-API-13: Actualizar aeropuerto (PUT /airports/{iata_code})
Objetivo: Verificar que un usuario autenticado como admin pueda actualizar la información de un aeropuerto.
"""

def test_update_airport_as_admin(admin_token, airport_iata_code):
    """
    TC-API-13: Actualizar aeropuerto.
    Este test recibe 'admin_token' y 'airport_iata' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    iata_code_to_update = airport_iata_code # El código IATA viene del fixture

    # 3. Preparar datos actualizados
    updated_data = {
        "iata_code": iata_code_to_update,
        "city": "Updated Test City",
        "country": "Updated Test Country"
    }

    # 4. Hacer la solicitud PUT a /airports/{iata_code}
    response = requests.put(f"{BASE_URL}/airports/{iata_code_to_update}", json=updated_data, headers=headers)

    # 5. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar actualizar el aeropuerto. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al actualizar aeropuerto. "
            f"Esperaba que los datos actualizados fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar actualizar el aeropuerto '{iata_code_to_update}'. "
            f"Esto indica que el aeropuerto no fue encontrado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de actualización exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al actualizar aeropuerto. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura y datos de la respuesta
    updated_airport = response.json()
    assert isinstance(updated_airport, dict), f"Se esperaba un diccionario, se obtuvo {type(updated_airport)}"

    # Verificar que los campos se hayan actualizado correctamente
    assert updated_airport["iata_code"] == iata_code_to_update, (
        f"El código IATA no debería cambiar. "
        f"Esperado: {iata_code_to_update}, Obtenido: {updated_airport['iata_code']}"
    )
    assert updated_airport["city"] == updated_data["city"], (
        f"La ciudad no se actualizó. "
        f"Esperado: {updated_data['city']}, Obtenido: {updated_airport['city']}"
    )
    assert updated_airport["country"] == updated_data["country"], (
        f"El país no se actualizó. "
        f"Esperado: {updated_data['country']}, Obtenido: {updated_airport['country']}"
    )

    print(f"✅ Aeropuerto actualizado exitosamente. IATA: {updated_airport['iata_code']}, Nueva Ciudad: "
          f"{updated_airport['city']}, Nuevo País: {updated_airport['country']}")

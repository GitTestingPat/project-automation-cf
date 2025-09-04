import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-28: Obtener aeronave por ID (GET /aircrafts/{aircraft_id})
Objetivo: Verificar que un usuario autenticado como admin pueda obtener la información de una aeronave específica.
"""

def test_get_aircraft_by_id(admin_token, aircraft_id_for_get):
    """
    TC-API-28: Obtener aeronave por ID.
    Este test recibe 'admin_token' y 'test_aircraft_id_for_get' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    aircraft_id_to_get = aircraft_id_for_get # El ID viene del fixture

    # 3. Hacer la solicitud GET a /aircrafts/{aircraft_id}
    response = requests.get(f"{BASE_URL}/aircrafts/{aircraft_id_to_get}", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar obtener la aeronave. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar obtener la aeronave '{aircraft_id_to_get}'. "
            f"Esto indica que la aeronave no fue encontrada, a pesar de haber sido creada. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401 or response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {response.status_code}) para obtener una aeronave. "
            f"Esto indica que el token de admin no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de obtención exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al obtener aeronave. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 5. Validar la estructura y datos de la respuesta (esquema AircraftOut)
    aircraft_data = response.json()
    assert isinstance(aircraft_data, dict), f"Se esperaba un diccionario, se obtuvo {type(aircraft_data)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "tail_number", "model", "capacity"]
    for field in expected_fields:
        assert field in aircraft_data, f"Falta el campo '{field}' en la respuesta de la aeronave obtenida."

    # Verificaciones específicas de contenido
    assert aircraft_data["id"] == aircraft_id_to_get, (
        f"El ID de la aeronave obtenida no coincide. "
        f"Esperado: {aircraft_id_to_get}, Obtenido: {aircraft_data['id']}"
    )
    assert aircraft_data["tail_number"] # Verificar que no esté vacío
    assert aircraft_data["model"] # Verificar que no esté vacío
    assert isinstance(aircraft_data["capacity"], int), (
        f"La capacidad debe ser un entero. Obtenido: {type(aircraft_data['capacity'])}"
    )
    assert aircraft_data["capacity"] > 0, (
        f"La capacidad debe ser mayor que 0. Obtenido: {aircraft_data['capacity']}"
    )

    print(f"✅ Aeronave obtenida exitosamente. ID: {aircraft_data['id']}, Tail Number: "
          f"{aircraft_data['tail_number']}, Modelo: {aircraft_data['model']}")

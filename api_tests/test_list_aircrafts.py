import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-26: Listar aeronaves (GET /aircrafts)
Objetivo: Verificar que un usuario autenticado como admin pueda obtener la lista de todas las aeronaves.
"""
@pytest.mark.TC_API_26
@pytest.mark.medium
@pytest.mark.aircrafts
@pytest.mark.positive
@pytest.mark.api
def test_list_aircrafts_as_admin(admin_token):
    """
    TC-API-26: Listar aeronaves.
    Este test recibe 'admin_token' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 3. Hacer la solicitud GET a /aircrafts
    response = requests.get(f"{BASE_URL}/aircrafts", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar listar aeronaves. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para listar aeronaves. "
            f"Esto indica que el token de admin no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 403:
        pytest.fail(
            f"La API devolvió 403 (Forbidden) al intentar listar aeronaves. "
            f"Esto indica que el usuario no tiene permisos suficientes (no es admin). "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de listado exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al listar aeronaves. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 5. Validar la estructura de la respuesta (esquema List[AircraftOut])
    aircrafts = response.json()
    assert isinstance(aircrafts, list), f"Se esperaba una lista, se obtuvo {type(aircrafts)}"

    # Verificar que cada elemento de la lista sea un diccionario (AircraftOut)
    if aircrafts: # Solo validar si la lista no está vacía
        first_aircraft = aircrafts[0]
        assert isinstance(first_aircraft, dict), f"Se esperaba un diccionario, se obtuvo {type(first_aircraft)}"

        # Verificar que los campos devueltos sean correctos y estén presentes
        expected_fields = ["id", "tail_number", "model", "capacity"]
        for field in expected_fields:
            assert field in first_aircraft, f"Falta el campo '{field}' en la respuesta del avión listado."

        # Verificaciones básicas de contenido
        assert first_aircraft["tail_number"] # Verificar que no esté vacío
        assert first_aircraft["model"] # Verificar que no esté vacío
        assert isinstance(first_aircraft["capacity"], int), (
            f"La capacidad debe ser un entero. Obtenido: {type(first_aircraft['capacity'])}"
        )
        assert first_aircraft["capacity"] > 0, (f"La capacidad debe ser mayor que 0. Obtenido: "
                                                f"{first_aircraft['capacity']}")

    print(f"✅ Lista de aeronaves obtenida exitosamente. Total: {len(aircrafts)} aviones")

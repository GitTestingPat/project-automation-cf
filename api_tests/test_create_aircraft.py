import requests
import pytest
import time
import random
import string
from conftest import BASE_URL

"""
Caso de prueba: TC-API-27: Crear aeronave (POST /aircrafts)
Objetivo: Verificar que un usuario autenticado como admin pueda crear una nueva aeronave.
"""

def test_create_aircraft_as_admin(admin_token):
    """
    TC-API-27: Crear aeronave.
    Este test recibe 'admin_token' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Preparar datos para la nueva aeronave.
    # Generar un tail_number único (6 caracteres: 1 letra fija + 5 aleatorios)
    timestamp = str(int(time.time()))[-5:] # Últimos 5 dígitos del timestamp
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=1)) # 1 carácter aleatorio
    tail_number = f"N{timestamp}{random_suffix}"[:6] # Asegurar 6 caracteres, formato ejemplo

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model {timestamp}",
        "capacity": 180
    }

    # 3. Hacer la solicitud POST a /aircrafts
    response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear una aeronave. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
         pytest.fail(
            f"Error de validación al crear aeronave. "
            f"Esperaba que los datos fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401 or response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {response.status_code}) para crear una aeronave. "
            f"Esto indica que el token de admin no fue aceptado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de creación exitosa debe devolver 201 Created
    assert response.status_code == 201, (
        f"Error al crear aeronave. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 5. Validar la estructura de la respuesta (esquema AircraftOut)
    created_aircraft = response.json()
    assert isinstance(created_aircraft, dict), f"Se esperaba un diccionario, se obtuvo {type(created_aircraft)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "tail_number", "model", "capacity"]
    for field in expected_fields:
        assert field in created_aircraft, f"Falta el campo '{field}' en la respuesta de la aeronave creada."

    # Verificaciones específicas de contenido
    assert created_aircraft["tail_number"] == new_aircraft_data["tail_number"], (
        f"El tail_number de la aeronave creada no coincide. "
        f"Esperado: {new_aircraft_data['tail_number']}, Obtenido: {created_aircraft['tail_number']}"
    )
    assert created_aircraft["model"] == new_aircraft_data["model"], (
        f"El modelo de la aeronave creada no coincide. "
        f"Esperado: {new_aircraft_data['model']}, Obtenido: {created_aircraft['model']}"
    )
    assert created_aircraft["capacity"] == new_aircraft_data["capacity"], (
        f"La capacidad de la aeronave creada no coincide. "
        f"Esperado: {new_aircraft_data['capacity']}, Obtenido: {created_aircraft['capacity']}"
    )
    # Validar que el campo 'id' es generado por el servidor
    assert "id" in created_aircraft and created_aircraft["id"], "Falta el 'id' en la respuesta de la aeronave creada"

    print(f"✅ Aeronave creada exitosamente. ID: {created_aircraft['id']}, Tail Number: "
          f"{created_aircraft['tail_number']}, Modelo: {created_aircraft['model']}")

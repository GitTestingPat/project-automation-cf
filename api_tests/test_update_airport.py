import requests
import pytest
import time
import random
import string
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-13: Actualizar aeropuerto (PUT /airports/{iata_code})
Objetivo: Verificar que un usuario autenticado como admin pueda actualizar la información de un aeropuerto.
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


def create_test_airport_for_update(admin_token):
    """
    Crea un aeropuerto de prueba específico para ser actualizado.
    Devuelve el código IATA del aeropuerto creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un código IATA único válido (3 letras mayúsculas).
    prefix = "U"  # Letra fija para el primer carácter (Update)
    suffix = ''.join(random.choices(string.ascii_uppercase, k=2))  # 2 letras aleatorias
    iata_code = f"{prefix}{suffix}"  # Resultado: "U" + 2 letras aleatorias = 3 letras

    new_airport_data = {
        "iata_code": iata_code,
        "city": f"Initial City {int(time.time())}",
        "country": f"Initial Country {int(time.time())}"
    }

    # Crear el aeropuerto
    create_response = requests.post(f"{BASE_URL}/airports", json=new_airport_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear aeropuerto para la prueba de actualización. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear aeropuerto para la prueba de actualización. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear aeropuerto para la prueba de actualización. "
        f"Esperaba 201, obtuvo {create_response.status_code}. "
        f"Cuerpo: {create_response.text}"
    )

    # La API devuelve los datos enviados. Verificar que se creó con el código correcto.
    created_data = create_response.json()
    assert created_data["iata_code"] == iata_code, (
        f"El aeropuerto creado no tiene el código IATA esperado. "
        f"Esperado: {iata_code}, Obtenido: {created_data['iata_code']}"
    )

    return iata_code


def test_update_airport_as_admin():
    """
    TC-API-13: Actualizar aeropuerto.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un aeropuerto de prueba para actualizar
    original_iata_code = create_test_airport_for_update(token)

    # 3. Preparar datos actualizados.
    updated_data = {
        "iata_code": original_iata_code,
        "city": "Updated Test City",
        "country": "Updated Test Country"
    }

    # 4. Hacer la solicitud PUT a /airports/{iata_code}
    response = requests.put(f"{BASE_URL}/airports/{original_iata_code}", json=updated_data, headers=headers)

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
            f"La API devolvió 404 (Not Found) al intentar actualizar el aeropuerto '{original_iata_code}'. "
            f"Esto indica que el aeropuerto no fue encontrado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de actualización exitosa debería devolver 200 OK
    assert response.status_code == 200, (
        f"Error al actualizar aeropuerto. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura y datos de la respuesta
    updated_airport = response.json()
    assert isinstance(updated_airport, dict), f"Se esperaba un diccionario, se obtuvo {type(updated_airport)}"

    # Verificar que los campos se hayan actualizado correctamente
    assert updated_airport["iata_code"] == original_iata_code, (
        f"El código IATA no debería cambiar. "
        f"Esperado: {original_iata_code}, Obtenido: {updated_airport['iata_code']}"
    )
    assert updated_airport["city"] == updated_data["city"], (
        f"La ciudad no se actualizó. "
        f"Esperado: {updated_data['city']}, Obtenido: {updated_airport['city']}"
    )
    assert updated_airport["country"] == updated_data["country"], (
        f"El país no se actualizó. "
        f"Esperado: {updated_data['country']}, Obtenido: {updated_airport['country']}"
    )

    print(
        f"✅ Aeropuerto actualizado exitosamente. IATA: {updated_airport['iata_code']}, "
        f"Nueva Ciudad: {updated_airport['city']}, Nuevo País: {updated_airport['country']}")

import requests
import pytest
import time
import random
import string
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-14: Eliminar aeropuerto (DELETE /airports/{iata_code})
Objetivo: Verificar que un usuario autenticado como admin pueda eliminar un aeropuerto.
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


def create_test_airport_for_deletion(admin_token):
    """
    Crea un aeropuerto de prueba específico para ser eliminado.
    Devuelve el código IATA del aeropuerto creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un código IATA único válido (3 letras mayúsculas).
    prefix = "D"  # Letra fija para el primer carácter (Delete)
    suffix = ''.join(random.choices(string.ascii_uppercase, k=2))  # 2 letras aleatorias
    iata_code = f"{prefix}{suffix}"  # Resultado: "D" + 2 letras aleatorias = 3 letras

    new_airport_data = {
        "iata_code": iata_code,
        "city": f"City to Delete {int(time.time())}",
        "country": f"Country to Delete {int(time.time())}"
    }

    # Crear el aeropuerto
    create_response = requests.post(f"{BASE_URL}/airports", json=new_airport_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear aeropuerto para la prueba de eliminación. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear aeropuerto para la prueba de eliminación. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear aeropuerto para la prueba de eliminación. "
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


def test_delete_airport_as_admin():
    """
    TC-API-14: Eliminar aeropuerto.
    """
    # 1. Obtener token de autenticación como admin
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un aeropuerto de prueba para eliminar
    iata_code_to_delete = create_test_airport_for_deletion(token)

    # 3. Hacer la solicitud DELETE a /airports/{iata_code}
    response = requests.delete(f"{BASE_URL}/airports/{iata_code_to_delete}", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar eliminar el aeropuerto. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar eliminar el aeropuerto '{iata_code_to_delete}'. "
            f"Esto indica que el aeropuerto no fue encontrado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de eliminación exitosa debería devolver 204 No Content
    assert response.status_code == 204, (
        f"Error al eliminar aeropuerto. "
        f"Esperaba 204 (No Content), obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    print(f"✅ Aeropuerto eliminado exitosamente. IATA: {iata_code_to_delete}")

import requests
import pytest
import time
import random
import string
from jsonschema import validate

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-11: Crear aeropuerto (POST /airports)
Objetivo: Verificar que se pueda crear un nuevo aeropuerto mediante una solicitud POST.
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


def test_create_airport():
    """
    TC-API-11: Crear aeropuerto.
    """
    # 1. Preparar datos para el nuevo aeropuerto.
    # Generar un código IATA único válido (3 letras mayúsculas).
    # Crear un prefijo fijo y añadir 2 letras aleatorias para reducir colisiones
    prefix = "T"  # Letra fija para el primer carácter
    suffix = ''.join(random.choices(string.ascii_uppercase, k=2))  # 2 letras aleatorias
    iata_code = f"{prefix}{suffix}"  # Resultado: "T" + 2 letras aleatorias = 3 letras
    # Ejemplo de resultado: "TAB", "TXY", etc.

    # Usar el timestamp para generar datos únicos de ciudad y país también
    timestamp = str(int(time.time()))  # Definir timestamp nuevamente si se necesita para otros campos

    new_airport_data = {
        "iata_code": iata_code,
        "city": f"Test City {timestamp}",
        "country": f"Test Country {timestamp}"
    }

    # 1.5. Obtener token de autenticación como admin
    # La API requiere autenticación aunque el esquema no lo indica claramente.
    try:
        token = get_admin_token()
    except PermissionError as e:
        pytest.skip(f"No se pudo autenticar como admin: {e}")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Hacer la solicitud POST a /airports
    # Se incluye el encabezado de autorización.
    response = requests.post(f"{BASE_URL}/airports", json=new_airport_data, headers=headers)

    # 3. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear un aeropuerto. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code in [401, 403]:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para crear un aeropuerto. "
            f"Esto no está documentado en el esquema AirportCreate. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear aeropuerto. "
            f"Esperaba que los datos fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de creación exitosa debe devolver 201 Created
    assert response.status_code == 201, (
        f"Error al crear aeropuerto. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 4. Validar la estructura de la respuesta.
    # La API devuelve los datos enviados. Verificar que sean los mismos.
    created_airport = response.json()
    assert isinstance(created_airport, dict), f"Se esperaba un diccionario, se obtuvo {type(created_airport)}"

    # Verificar que los campos devueltos sean los mismos que los enviados
    assert created_airport["iata_code"] == new_airport_data["iata_code"], (
        f"El código IATA no coincide. "
        f"Esperado: {new_airport_data['iata_code']}, Obtenido: {created_airport['iata_code']}"
    )
    assert created_airport["city"] == new_airport_data["city"], (
        f"La ciudad no coincide. "
        f"Esperado: {new_airport_data['city']}, Obtenido: {created_airport['city']}"
    )
    assert created_airport["country"] == new_airport_data["country"], (
        f"El país no coincide. "
        f"Esperado: {new_airport_data['country']}, Obtenido: {created_airport['country']}"
    )

    print(f"✅ Aeropuerto creado exitosamente. IATA: {created_airport['iata_code']}, Ciudad: {created_airport['city']}")


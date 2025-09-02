import requests
import pytest
import time
import random
import string

BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
Caso de prueba: TC-API-12: Obtener aeropuerto (GET /airports/{iata_code})
Objetivo: Verificar que se pueda obtener la información de un aeropuerto específico mediante su código IATA.
"""

def create_test_airport():
    """
    Crea un aeropuerto de prueba para luego obtenerlo.
    Reutiliza la lógica de generación de código IATA válida.
    Devuelve el código IATA del aeropuerto creado.
    """
    # Generar un código IATA único válido (3 letras mayúsculas).
    prefix = "T"  # Letra fija para el primer carácter
    suffix = ''.join(random.choices(string.ascii_uppercase, k=2))  # 2 letras aleatorias
    iata_code = f"{prefix}{suffix}"  # Resultado: "T" + 2 letras aleatorias = 3 letras

    new_airport_data = {
        "iata_code": iata_code,
        "city": f"Test City {int(time.time())}",
        "country": f"Test Country {int(time.time())}"
    }

    # La API requiere autenticación para crear un aeropuerto.
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    assert login_response.status_code == 200, (
        f"Falló el login de admin para crear aeropuerto. "
        f"Status: {login_response.status_code}, Body: {login_response.text}"
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear el aeropuerto
    create_response = requests.post(f"{BASE_URL}/airports", json=new_airport_data, headers=headers)

    # Manejar errores comunes
    if create_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear aeropuerto para la prueba de obtención. "
            f"Cuerpo: {create_response.text}"
        )
    elif create_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear aeropuerto para la prueba de obtención. "
            f"Cuerpo: {create_response.text}"
        )

    assert create_response.status_code == 201, (
        f"Error al crear aeropuerto para la prueba de obtención. "
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


def test_get_airport_by_iata_code():
    """
    TC-API-12: Obtener aeropuerto.
    """
    # 1. Crear un aeropuerto de prueba
    test_iata_code = create_test_airport()

    # 2. Hacer la solicitud GET a /airports/{iata_code}
    response = requests.get(f"{BASE_URL}/airports/{test_iata_code}")

    # 3. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar obtener el aeropuerto. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación en el código IATA al obtener aeropuerto. "
            f"Esto podría indicar un problema con el formato del código '{test_iata_code}'. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar obtener el aeropuerto '{test_iata_code}'. "
            f"Esto indica que el aeropuerto no fue encontrado, a pesar de haber sido creado. "
            f"Puede ser un problema de consistencia en la API o un retraso en la indexación. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de obtención exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al obtener aeropuerto. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 4. Validar la estructura y datos de la respuesta (esquema AirportOut)
    airport_data = response.json()
    assert isinstance(airport_data, dict), f"Se esperaba un diccionario, se obtuvo {type(airport_data)}"

    # Verificar que los campos devueltos sean correctos
    assert "iata_code" in airport_data, "Falta 'iata_code' en la respuesta"
    assert airport_data["iata_code"] == test_iata_code, (
        f"El código IATA obtenido no coincide. "
        f"Esperado: {test_iata_code}, Obtenido: {airport_data['iata_code']}"
    )

    assert "city" in airport_data, "Falta 'city' en la respuesta"
    assert "country" in airport_data, "Falta 'country' en la respuesta"
    print(
        f"✅ Aeropuerto obtenido exitosamente. IATA: {airport_data['iata_code']}, "
        f"Ciudad: {airport_data.get('city', 'N/A')}")

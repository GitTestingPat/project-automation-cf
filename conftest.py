import time
import uuid
import requests
import pytest
from selenium import webdriver
import os
from datetime import datetime, timezone, timedelta
from jsonschema import validate
import random
import string
from selenium.webdriver.chrome.options import Options

"""
Archivo de configuración global para pytest.
Contiene fixtures reutilizables y hooks personalizados.
"""

# --- Configuración Global ---
BASE_URL = "https://cf-automation-airline-api.onrender.com"

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


# --- Hooks de Pytest ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook personalizado para tomar un screenshot automáticamente cuando una prueba de Selenium falla.
    """
    # Ejecutar la prueba y obtener el resultado
    outcome = yield
    report = outcome.get_result()

    # Solo actuar si la prueba falló durante la fase de ejecución ("call")
    if report.when == "call" and report.failed:
        # Intentar obtener la instancia del driver de Selenium
        driver = None
        try:
            # Asumir que la prueba lo pasó como argumento o lo tiene como atributo self.driver
            if hasattr(item, 'funcargs'):
                # Si la prueba usa el fixture 'driver' como argumento
                driver = item.funcargs.get('driver')
            if driver is None and hasattr(item.instance, 'driver'):
                # Si la prueba es un metodo de una clase y la clase tiene self.driver
                driver = item.instance.driver
        except Exception:
            # Silenciar errores al intentar obtener el driver
            pass

        # Si se encontró un driver válido, tomar el screenshot
        if driver is not None:
            try:
                # Asegurarse de que la carpeta de screenshots exista
                os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

                # Generar un nombre de archivo único con timestamp y nombre de la prueba
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_test_name = "".join(c for c in item.name if c.isalnum() or c in (' ', '_')).rstrip()
                screenshot_filename = f"{safe_test_name}_{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)

                # Tomar y guardar el screenshot
                success = driver.save_screenshot(screenshot_path)

                if success:
                    print(f"\n📸 Screenshot guardado en: {screenshot_path}")
                else:
                    print(f"\n⚠️ No se pudo guardar el screenshot en: {screenshot_path}")
            except Exception as e:
                # Silenciar errores al tomar el screenshot, pero registrarlos
                print(f"\n❌ Error al intentar tomar screenshot: {e}")


# --- Fixtures ---

@pytest.fixture
def auth_token():
    """
    Fixture que registra un nuevo usuario de prueba y devuelve su token JWT.
    """
    # Generar email único usando uuid4 para evitar colisiones
    email = f"user_{uuid.uuid4()}@test.com"
    password = "SecurePass123!"
    full_name = "Test User"

    # 1. Registrar usuario
    signup_data = {"email": email, "password": password, "full_name": full_name}
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Error de red al intentar registrar usuario: {e}")

    # Aceptar error 500 y saltar la prueba
    if signup_response.status_code == 500:
        error_detail = signup_response.text
        pytest.skip(
            f"El endpoint /auth/signup devolvió 500. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {error_detail}"
        )

    if signup_response.status_code != 201:
        pytest.fail(
            f"Error al registrar usuario de prueba en la fixture 'auth_token'. "
            f"Esperaba 201, obtuvo {signup_response.status_code}. "
            f"Payload enviado: {signup_data}. "
            f"Cuerpo de la respuesta: {signup_response.text}"
        )

    # 2. Hacer login
    login_data = {"username": email, "password": password}
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Error de red al intentar iniciar sesión: {e}")

    if login_response.status_code != 200:
        pytest.fail(
            f"Error al iniciar sesión con el usuario de prueba en la fixture 'auth_token'. "
            f"Esperaba 200, obtuvo {login_response.status_code}. "
            f"Payload enviado: {login_data}. "
            f"Cuerpo de la respuesta: {login_response.text}"
        )

    token_data = login_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        pytest.fail(
            f"No se obtuvo 'access_token' al iniciar sesión en la fixture 'auth_token'. "
            f"Datos del token recibidos: {token_data}"
        )

    return access_token

@pytest.fixture
def user_token():
    """
    Fixture que crea un nuevo usuario de prueba y devuelve su token de acceso.
    Se ejecuta una vez por prueba que lo requiere.
    """
    # Generar un email único
    timestamp = str(int(time.time()))[-5:]
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    test_email = f"fixture_user_{timestamp}_{random_suffix}@test.com"
    test_password = "SecurePass123!"

    user_data = {
        "email": test_email,
        "password": test_password,
        "full_name": f"Fixture Tester {timestamp}"
    }

    # Registrar el nuevo usuario
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Error de red al intentar registrar usuario en fixture 'user_token': {e}")

    # Manejar posibles errores durante el registro
    if signup_response.status_code == 201:
        # Registro exitoso
        print(f"✅ Usuario de prueba creado en fixture 'user_token': {test_email}")
    elif signup_response.status_code == 400:
        error_detail = signup_response.json().get("detail", "")
        if "already registered" in str(error_detail).lower():
            # Aunque sea improbable con el email único, manejar errores
            pytest.fail(
                f"Error inesperado en fixture 'user_token': El email '{test_email}' ya estaba registrado. "
                f"Esto es inusual con un email generado. "
                f"Detalle: {error_detail}"
            )
        else:
            pytest.fail(
                f"Error 400 en fixture 'user_token' al crear usuario de prueba. "
                f"Detalle: {error_detail}"
            )
    elif signup_response.status_code == 500:
         pytest.skip(
            f"La API devolvió un error 500 en fixture 'user_token' al intentar crear un usuario de prueba. "
            f"Esto indica un posible fallo interno en el servidor de la API. "
            f"Cuerpo de la respuesta: {signup_response.text}"
        )
    else:
        # Manejar otro error inesperado
        pytest.fail(
            f"Error inesperado en fixture 'user_token' al crear usuario de prueba. "
            f"Status: {signup_response.status_code}, "
            f"Body: {signup_response.text}"
        )

    # Iniciar sesión con el usuario recién creado
    login_data = {
        "username": test_email,
        "password": test_password
    }
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    except requests.exceptions.RequestException as e:
         pytest.skip(f"Error de red en fixture 'user_token' al intentar iniciar sesión: {e}")

    if login_response.status_code == 200:
        token_data = login_response.json()
        return token_data["access_token"]
    else:
        # Indica si el login falla después de crear el usuario
        pytest.fail(
            f"Falló el login en fixture 'user_token' del usuario de prueba recién creado. "
            f"Status: {login_response.status_code}, Body: {login_response.text}. "
            f"Esto indica un problema inesperado después de la creación."
        )

@pytest.fixture
def driver():
    """
    Fixture que configura y proporciona una instancia del driver de Selenium (Chrome). Pruebas de Web UI.
    """
    options = webdriver.ChromeOptions()

    # ✅ Opciones para entornos locales y CI (GitHub Actions)
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    # Opción adicional para evitar problemas de zona horaria en CI
    options.add_argument("--timezone=UTC")

    # Iniciar el driver
    driver = webdriver.Chrome(options=options)
    # Establecer un tiempo de espera implícito estándar
    driver.implicitly_wait(10)
    yield driver

    # Código de limpieza: cerrar el driver al finalizar la prueba
    try:
        driver.quit()
    except:
        # Silenciar errores al cerrar
        pass


# --- Fixtures para Recursos de Prueba Específicos ---

@pytest.fixture(scope="session")
def admin_token():
    """
    Fixture que obtiene un token JWT para el usuario administrador preexistente.
    Se reutiliza para todas las pruebas que lo necesiten dentro de una sesión.
    """
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Error de red al intentar iniciar sesión como admin: {e}")

    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        pytest.skip(
            f"No se pudo obtener el token de admin. "
            f"Status: {response.status_code}, Body: {response.text}. "
            f"Esto puede deberse a credenciales incorrectas o a un fallo en la API de prueba."
        )


@pytest.fixture
def aircraft_id(admin_token):
    """
    Fixture que crea un avión de prueba y devuelve su ID.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Generar un tail_number único
    timestamp = str(int(time.time()))[-5:]
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    tail_number = f"N{timestamp}{random_suffix}"[:6]  # Asegurar 6 caracteres

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model {timestamp}",
        "capacity": 150
    }
    try:
        response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error de red al crear avión de prueba: {e}")

    # Manejar errores comunes durante la creación
    if response.status_code == 500:
        error_detail = response.text
        pytest.skip(
            f"La API devolvió un 500 al crear avión de prueba en la fixture 'aircraft_id'. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {error_detail}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear avión de prueba en la fixture 'aircraft_id'. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 201, (
        f"Error al crear avión de prueba en la fixture 'aircraft_id'. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    created_aircraft = response.json()
    assert "id" in created_aircraft, "Falta 'id' en la respuesta del avión creado."
    return created_aircraft["id"]


@pytest.fixture
def flight_id(admin_token, aircraft_id):
    """
    Fixture que crea un vuelo de prueba y devuelve su ID.
    Requiere las fixtures 'admin_token' y 'aircraft_id'.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    future_time = datetime.now(timezone.utc) + timedelta(hours=1)
    arrival_time = future_time + timedelta(hours=2)

    new_flight_data = {
        "origin": "MEX",
        "destination": "BCN",
        "departure_time": future_time.isoformat(),
        "arrival_time": arrival_time.isoformat(),
        "base_price": 599.99,
        "aircraft_id": aircraft_id
    }
    try:
        response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=headers)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error de red al crear vuelo de prueba: {e}")

    # Manejar errores comunes durante la creación
    # La operación de creación exitosa debe devolver 201 Created.
    # La API puede devolver 200 OK intermitentemente en lugar de 201.
    # Comportamiento no estándar pero simulado/intermitente.
    # Aceptar ambos códigos.
    if response.status_code not in [200, 201]:
        # Manejar errores específicos
        if response.status_code == 500:
            error_detail = response.text
            pytest.skip(
                f"La API devolvió un 500 al crear vuelo en la fixture 'flight_id'. "
                f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
                f"Cuerpo de la respuesta: {error_detail}"
            )
        elif response.status_code == 422:
            pytest.fail(
                f"Error de validación al crear vuelo en la fixture 'flight_id'. "
                f"Cuerpo de la respuesta: {response.text}"
            )
        elif response.status_code == 401 or response.status_code == 403:
            pytest.skip(
                f"La API requirió autenticación/permisos (Status: {response.status_code}) para crear un vuelo. "
                f"Esto indica que el token de admin no fue aceptado. "
                f"Cuerpo de la respuesta: {response.text}"
            )
        elif response.status_code == 404:
             pytest.fail(
                f"La API devolvió 404 (Not Found) al intentar crear un vuelo. "
                f"Esto indica que el endpoint no fue encontrado. "
                f"Cuerpo de la respuesta: {response.text}"
            )

        # Si no es ninguno de los códigos manejados específicamente, es un error inesperado
        pytest.fail(
            f"Error al crear vuelo en la fixture 'flight_id'. "
            f"Esperaba 200 o 201, obtuvo {response.status_code}. "
            f"Cuerpo: {response.text}"
        )
    # Si el código es 200 o 201, continuar normalmente
    created_flight = response.json()
    assert "id" in created_flight, "Falta 'id' en la respuesta del vuelo creado."
    return created_flight["id"]


# --- Fixture para crear una reserva de prueba ---
@pytest.fixture
def booking_id(user_token, flight_id):
    """
    Fixture que crea una reserva de prueba para un vuelo dado y un usuario autenticado.
    Devuelve el ID de la reserva creada.
    """
    headers = {"Authorization": f"Bearer {user_token}"}

    # Datos para la nueva reserva
    new_booking_data = {
        "flight_id": flight_id,
        "passengers": [
            {
                "full_name": "Pasajero de Prueba Fixture",
                "passport": "P12345678"
            }
        ]
    }

    # Crear la reserva
    try:
        response = requests.post(f"{BASE_URL}/bookings", json=new_booking_data, headers=headers)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error de red al crear reserva de prueba: {e}")

    # Manejar errores comunes durante la creación
    if response.status_code == 500:
        error_detail = response.text
        pytest.skip(
            f"La API devolvió un 500 al crear reserva en la fixture 'booking_id'. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {error_detail}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear reserva en la fixture 'booking_id'. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para crear una reserva en la fixture. "
            f"Esto indica que el token de usuario no fue aceptado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 201, (
        f"Error al crear reserva en la fixture 'booking_id'. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    created_booking = response.json()
    assert "id" in created_booking, "Falta 'id' en la respuesta de la reserva creada por la fixture."
    return created_booking["id"]

@pytest.fixture
def airport_iata_code(admin_token):
    """
    Fixture que crea un aeropuerto de prueba y devuelve su código IATA.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Generar un código IATA único (3 letras mayúsculas)
    prefix = "T"  # Letra fija para el primer carácter
    suffix = ''.join(random.choices(string.ascii_uppercase, k=2))  # 2 letras aleatorias
    iata_code = f"{prefix}{suffix}"  # Resultado: "T" + 2 letras aleatorias = 3 letras

    new_airport_data = {
        "iata_code": iata_code,
        "city": f"Test City {int(time.time())}",
        "country": "Test Country"
    }

    # Crear el aeropuerto
    try:
        response = requests.post(f"{BASE_URL}/airports", json=new_airport_data, headers=headers)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error de red al crear aeropuerto de prueba: {e}")

    # Manejar errores comunes durante la creación
    if response.status_code == 500:
        error_detail = response.text
        pytest.skip(
            f"La API devolvió un 500 al crear aeropuerto en la fixture 'airport_iata_code'. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {error_detail}"
        )
    elif response.status_code == 422:
         pytest.fail(
            f"Error de validación al crear aeropuerto en la fixture 'airport_iata_code'. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401 or response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {response.status_code}) para crear un aeropuerto. "
            f"Esto indica que el token de admin no fue aceptado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 201, (
        f"Error al crear aeropuerto en la fixture 'airport_iata_code'. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    created_airport = response.json()
    assert "iata_code" in created_airport, "Falta 'iata_code' en la respuesta del aeropuerto creado."
    assert created_airport["iata_code"] == iata_code, (
        f"El código IATA del aeropuerto creado no coincide. "
        f"Esperado: {iata_code}, Obtenido: {created_airport['iata_code']}"
    )
    return created_airport["iata_code"]

@pytest.fixture
def user_id_to_delete(admin_token):
    """
    Fixture que crea un usuario de prueba específico para ser eliminado.
    Devuelve el ID del usuario creado.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Generar un email único
    import random
    import string
    timestamp = str(int(time.time()))[-5:]
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    test_email = f"user_to_delete_{timestamp}_{random_suffix}@test.com"
    test_password = "ToDeletePass123!"
    full_name = f"User to Delete {timestamp}"

    user_data = {
        "email": test_email,
        "password": test_password,
        "full_name": full_name,
        "role": "passenger" # Rol opcional, por defecto es passenger
    }

    # Crear el usuario
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=headers)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error de red al crear usuario de prueba para eliminar: {e}")

    # Manejar errores comunes durante la creación
    if response.status_code == 500:
        error_detail = response.text
        pytest.skip(
            f"La API devolvió un 500 al crear usuario en la fixture 'user_id_to_delete'. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {error_detail}"
        )
    elif response.status_code == 422:
         pytest.fail(
            f"Error de validación al crear usuario en la fixture 'user_id_to_delete'. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401 or response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {response.status_code}) para crear un usuario. "
            f"Esto indica que el token de admin no fue aceptado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 201, (
        f"Error al crear usuario en la fixture 'user_id_to_delete'. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    created_user = response.json()
    assert "id" in created_user, "Falta 'id' en la respuesta del usuario creado."

    return created_user["id"]

@pytest.fixture
def new_user_data():
    """
    Fixture que genera un diccionario con datos únicos para crear un nuevo usuario.
    Devuelve un diccionario con 'email', 'password', 'full_name' y 'role'.
    """
    # Generar un email único
    timestamp = str(int(time.time()))[-5:]
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    test_email = f"new_user_{timestamp}_{random_suffix}@test.com"
    test_password = "SecureNewPass123!"
    full_name = f"New User {timestamp}"

    # Especificar un rol
    role = "passenger"

    user_data = {
        "email": test_email,
        "password": test_password,
        "full_name": full_name,
        "role": role
    }

    return user_data

@pytest.fixture
def payment_id(user_token, booking_id):
    """
    Fixture que crea un pago de prueba y devuelve su ID.
    Requiere las fixtures 'user_token' y 'test_booking_id'.
    """
    headers = {"Authorization": f"Bearer {user_token}"}
    booking_id_to_pay = booking_id

    # 1. Preparar datos para el nuevo pago.
    new_payment_data = {
        "booking_id": booking_id_to_pay,
        "amount": 299.99,
        "payment_method": "credit_card" # Método de pago de ejemplo
    }

    # 2. Crear el pago
    try:
        response = requests.post(f"{BASE_URL}/payments", json=new_payment_data, headers=headers)
    except requests.exceptions.RequestException as e:
         pytest.fail(f"Error de red al crear pago de prueba: {e}")

    # Manejar errores comunes durante la creación
    if response.status_code == 500:
        error_detail = response.text
        pytest.skip(
            f"La API devolvió un error 500 al crear pago en la fixture 'payment_id'. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {error_detail}"
        )
    elif response.status_code == 422:
         pytest.fail(
            f"Error de validación al crear pago en la fixture 'payment_id'. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para crear un pago. "
            f"Esto indica que el token de usuario no fue aceptado. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar crear un pago para la reserva '{booking_id_to_pay}'. "
            f"Esto indica que la reserva no fue encontrada. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 201, (
        f"Error al crear pago en la fixture 'payment_id'. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    created_payment = response.json()
    assert "id" in created_payment, "Falta 'id' en la respuesta del pago creado."
    return created_payment["id"]


@pytest.fixture
def aircraft_id_for_get(admin_token):
    """
    Fixture que crea una aeronave de prueba específica para la prueba de obtención por ID.
    Recibe la fixture 'admin_token'.
    Devuelve el ID de la aeronave creada.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Generar un tail_number único
    import random
    import string
    timestamp = str(int(time.time()))[-5:]
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    tail_number = f"N{timestamp}AG"  # Asegurar 6 caracteres

    new_aircraft_data = {
        "tail_number": tail_number,
        "model": f"Test Model Get {timestamp}",
        "capacity": 180
    }

    # Crear la aeronave
    try:
        response = requests.post(f"{BASE_URL}/aircrafts", json=new_aircraft_data, headers=headers)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Error de red al crear aeronave de prueba para obtención: {e}")

    # Manejar errores comunes durante la creación
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear aeronave en la fixture 'aircraft_id_for_get'. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear aeronave en la fixture 'aircraft_id_for_get'. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401 or response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {response.status_code}) para crear una aeronave. "
            f"Esto indica que el token de admin no fue aceptado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    assert response.status_code == 201, (
        f"Error al crear aeronave en la fixture 'aircraft_id_for_get'. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo: {response.text}"
    )

    created_aircraft = response.json()
    assert "id" in created_aircraft, "Falta 'id' en la respuesta de la aeronave creada."
    assert created_aircraft["tail_number"] == tail_number, (
        f"El tail_number de la aeronave creada no coincide. "
        f"Esperado: {tail_number}, Obtenido: {created_aircraft['tail_number']}"
    )

    return created_aircraft["id"]

@pytest.fixture
def create_test_booking_for_listing(user_token, admin_token, aircraft_id):
    """
    Crea una reserva de prueba para luego listarla.
    Requiere 'user_token', 'admin_token' y 'aircraft_id' de las fixtures.
    Devuelve el ID de la reserva creada.
    """
    user_headers = {"Authorization": f"Bearer {user_token}"}
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Crear un vuelo de prueba usando el avión proporcionado por la fixture
    future_time = datetime.now(timezone.utc) + timedelta(hours=12)
    arrival_time = future_time + timedelta(hours=13)

    new_flight_data = {
        "origin": "MAD",  # Código IATA válido
        "destination": "FCO",  # Código IATA válido
        "departure_time": future_time.isoformat(),
        "arrival_time": arrival_time.isoformat(),
        "base_price": 399.99,
        "aircraft_id": aircraft_id  # ID del avión viene del fixture
    }

    # Crear el vuelo
    create_flight_response = requests.post(f"{BASE_URL}/flights", json=new_flight_data, headers=admin_headers)

    # Manejar errores comunes durante la creación del vuelo
    if create_flight_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear vuelo para la prueba de listado de reservas. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {create_flight_response.text}"
        )
    elif create_flight_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear vuelo para la prueba de listado de reservas. "
            f"Cuerpo de la respuesta: {create_flight_response.text}"
        )
    elif create_flight_response.status_code == 401 or create_flight_response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {create_flight_response.status_code}) "
            f"para crear un vuelo. "
            f"Esto indica que el token de admin no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {create_flight_response.text}"
        )

    assert create_flight_response.status_code == 201, (
        f"Error al crear vuelo para la prueba de listado de reservas. "
        f"Esperaba 201, obtuvo {create_flight_response.status_code}. "
        f"Cuerpo de la respuesta: {create_flight_response.text}"
    )

    created_flight = create_flight_response.json()
    assert "id" in created_flight, "Falta 'id' en la respuesta del vuelo creado."
    flight_id = created_flight["id"]

    # 2. Preparar datos para la nueva reserva.
    new_booking_data = {
        "flight_id": flight_id,
        "passengers": [
            {
                "full_name": "Pasajero Para Listar",
                "passport": "P11111111"
            }
        ]
    }

    # 3. Crear la reserva
    create_booking_response = requests.post(f"{BASE_URL}/bookings", json=new_booking_data, headers=user_headers)

    # Manejar errores comunes durante la creación de la reserva
    if create_booking_response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 al crear reserva para la prueba de listado. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {create_booking_response.text}"
        )
    elif create_booking_response.status_code == 422:
        pytest.fail(
            f"Error de validación al crear reserva para la prueba de listado. "
            f"Cuerpo de la respuesta: {create_booking_response.text}"
        )
    elif create_booking_response.status_code == 401 or create_booking_response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {create_booking_response.status_code}) "
            f"para crear una reserva. "
            f"Esto indica que el token de usuario no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {create_booking_response.text}"
        )

    assert create_booking_response.status_code == 201, (
        f"Error al crear reserva para la prueba de listado. "
        f"Esperaba 201, obtuvo {create_booking_response.status_code}. "
        f"Cuerpo de la respuesta: {create_booking_response.text}"
    )

    created_booking = create_booking_response.json()
    assert "id" in created_booking, "Falta 'id' en la respuesta de la reserva creada."
    return created_booking["id"]
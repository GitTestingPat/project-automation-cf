import pytest
from selenium import webdriver
import os
from datetime import datetime

BASE_URL = "https://cf-automation-airline-api.onrender.com"

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

@pytest.fixture
def auth_token():
    """Fixture que registra un usuario y devuelve un token JWT"""
    # Generar datos únicos
    timestamp = int(time.time())
    email = f"user_{timestamp}@test.com"
    password = "123456"
    full_name = "Test User"

    # 1. Registrar usuario
    signup_data = {"email": email, "password": password, "full_name": full_name}
    signup_response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)

    assert signup_response.status_code == 201, f"Error en signup: {signup_response.text}"

    # 2. Hacer login
    login_data = {"username": email, "password": password}
    login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    assert login_response.status_code == 200, f"Error en login: {login_response.text}"
    token = login_response.json()["access_token"]

    return token


@pytest.fixture
def driver():
    """Fixture para crear un driver de Selenium con opciones comunes"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Generar un screenshot automáticamente cuando una prueba de Selenium falla.
    """
    # Obtener el resultado de la ejecución de la prueba
    outcome = yield
    report = outcome.get_result()

    # Verificar si la prueba ha fallado durante la fase de ejecución ('call')
    if report.when == "call" and report.failed:
        # Obtener la instancia del driver de Selenium utilizada en la prueba
        driver = None

        # Intentar recuperar el driver desde los argumentos de la función de prueba (fixture)
        if hasattr(item, 'funcargs'):
            driver = item.funcargs.get('driver')

        # Fallback: Intentar recuperar el driver como atributo de la instancia de la clase de prueba
        if driver is None:
            driver = getattr(item.instance, 'driver', None)

        # Si se encuentra el driver, proceder a tomar el screenshot
        if driver:
            # Crear el directorio de screenshots si no existe
            os.makedirs("screenshots", exist_ok=True)

            # Generar una ruta de archivo única para el screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join("screenshots", screenshot_filename)

            # Guardar el screenshot usando el driver de Selenium
            try:
                driver.save_screenshot(screenshot_path)
            except Exception:
                # Silenciar errores al tomar el screenshot para no afectar el resultado de la prueba
                pass
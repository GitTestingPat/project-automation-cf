import time
import uuid
import requests
import pytest
from selenium import webdriver
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://cf-automation-airline-api.onrender.com"

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

@pytest.fixture
def auth_token():
    """Fixture que registra un usuario y devuelve un token JWT"""
    # Generar email único usando uuid4 para evitar colisiones
    email = f"user_{uuid.uuid4()}@test.com"
    password = "123456"
    full_name = "Test User"

    # 1. Registrar usuario
    signup_data = {"email": email, "password": password, "full_name": full_name}
    signup_response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)

    # Mejorar diagnóstico en caso de error
    if signup_response.status_code != 201:
        print("ERROR en signup:")
        print("Payload enviado:", signup_data)
        print("Respuesta:", signup_response.text)
        raise AssertionError(f"Error en signup ({signup_response.status_code}): {signup_response.text}")

    # 2. Hacer login
    login_data = {"username": email, "password": password}
    login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    if login_response.status_code != 200:
        print("ERROR en login:")
        print("Payload enviado:", login_data)
        print("Respuesta:", login_response.text)
        raise AssertionError(f"Error en login ({login_response.status_code}): {login_response.text}")

    token = login_response.json().get("access_token")
    if not token:
        raise AssertionError(f"No se obtuvo token en login: {login_response.text}")

    return token


@pytest.fixture
def driver():
    """Fixture para crear un driver de Selenium con opciones comunes"""
    options = Options()
    options.add_argument(f"--user-data-dir=/tmp/chrome_profile_{uuid.uuid4()}")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Generar un screenshot automáticamente cuando una prueba de Selenium falla.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = None
        if hasattr(item, 'funcargs'):
            driver = item.funcargs.get('driver')
        if driver is None:
            driver = getattr(item.instance, 'driver', None)
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join("screenshots", screenshot_filename)
            try:
                driver.save_screenshot(screenshot_path)
            except Exception:
                pass
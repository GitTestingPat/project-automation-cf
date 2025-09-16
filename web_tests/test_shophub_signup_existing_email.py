import requests
import pytest
import time
from selenium.webdriver.common.by import By
from pages.shophub_home_page import HomePage
from pages.shophub_signup_page import SignupPage

"""
Caso de prueba: TC-WEB-07: Registrar con email ya existente (Negativo)
Objetivo: Verificar que la página de registro muestre un mensaje de error al intentar registrar un email que ya existe.
"""

def test_register_with_existing_email(driver):
    """
    TC-WEB-07: Registrar con email ya existente (Negativo).
    Este test recibe 'driver' del fixture.
    """
    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Hacer clic en "Sign Up"
    signup_page = home_page.click_sign_up()

    # 3. Preparar datos para el registro con email existente.
    # Usar un email que ya existe en la API.
    existing_email = "admin@demo.com"
    test_password = "SecurePass123!"
    full_name = "Test User Existing"

    # 4. Llenar el formulario de registro con datos de email existente
    signup_page.enter_first_name("Test")
    signup_page.enter_last_name("User Existing")
    signup_page.enter_email(existing_email)
    signup_page.enter_zip_code("12345")
    signup_page.enter_password(test_password)
    signup_page.click_sign_up()

    # 5. Verificar que se muestre un mensaje de error.
    # Manejar errores comunes
    try:
        error_message_element = driver.find_element(By.CSS_SELECTOR, ".error-message, .alert-danger")
        error_message_text = error_message_element.text
    except:
        pytest.fail(
            f"No se encontró un mensaje de error después de intentar registrar con email existente '{existing_email}'. "
            f"Esto indica que la página no mostró feedback al usuario sobre el fallo. "
            f"Posible fallo en la validación del lado del cliente o del servidor. "
            f"Verifica que el selector '.error-message' o '.alert-danger' sea correcto para la página de ShopHub."
        )

    # Verificar que el mensaje de error sea el esperado
    assert "already registered" in error_message_text.lower() or "exists" in error_message_text.lower(), (
        f"El mensaje de error no indica claramente que el email ya está registrado. "
        f"Esperaba un mensaje que contenga 'already registered' o 'exists'. "
        f"Obtenido: '{error_message_text}'. "
        f"Esto indica que el mensaje de error no es claro o descriptivo para el usuario."
    )

    print(f"✅ Registro rechazado correctamente por email existente. Mensaje: {error_message_text}")

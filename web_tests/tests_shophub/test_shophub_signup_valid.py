import pytest
import time
import random
import string
from selenium.webdriver.common.by import By
from pages.shophub.shophub_home_page import HomePage

"""
Caso de prueba: TC-WEB-06: Registrar nuevo usuario con datos válidos
Objetivo: Verificar que un nuevo usuario pueda registrarse exitosamente en ShopHub usando credenciales válidas.
"""


def test_register_new_user_with_valid_credentials(driver):
    """
    TC-WEB-06: Registrar nuevo usuario con datos válidos.
    Este test recibe 'driver' del fixture.
    """
    # 1. Ir a la página principal de ShopHub
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Hacer clic en el enlace "Sign Up"
    signup_page = home_page.click_sign_up()

    # 3. Preparar datos únicos para el nuevo usuario.
    # Generar un email único para evitar conflictos con usuarios ya registrados
    timestamp = str(int(time.time()))[-5:]
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    test_email = f"new_user_{timestamp}_{random_suffix}@test.com"
    test_password = "SecurePass123!"
    first_name = f"NewUser{timestamp}"
    last_name = f"Test{random_suffix}"

    # 4. Llenar el formulario de registro con los datos del nuevo usuario
    signup_page.enter_first_name(first_name)
    signup_page.enter_last_name(last_name)
    signup_page.enter_email(test_email)
    signup_page.enter_zip_code("12345")
    signup_page.enter_password(test_password)
    signup_page.click_sign_up()

    # 5. Verificar que el registro sea exitoso.
    # Manejar posibles errores comunes durante el registro
    # (Por ejemplo, si la página muestra un mensaje de error en lugar de redirigir)

    # Verificar que se redirija a la página de login
    expected_title_after_signup = "Login"
    if expected_title_after_signup.lower() in driver.title.lower():
        print(f"✅ Registro exitoso. Redirigido a la página de login. Título: {driver.title}")
        return  # Salir de la prueba, ya que el registro fue exitoso

    # Verificar que aparezca un mensaje de éxito en la misma página
    try:
        success_message_element = driver.find_element(By.CSS_SELECTOR, ".alert-success, .success-message")
        success_message_text = success_message_element.text
        if "successfully" in success_message_text.lower() or "welcome" in success_message_text.lower():
            print(f"✅ Registro exitoso. Mensaje de éxito: {success_message_text}")
            return  # Salir de la prueba, ya que el registro fue exitoso
    except:
        # Si no se encuentra el mensaje de éxito, continuar con otras verificaciones
        pass

    # Verificar que el botón de "Sign Up" ya no esté presente
    try:
        signup_button = driver.find_element(*signup_page.SIGN_UP_BUTTON)
        # Si el botón sigue presente, el registro puede no haber sido exitoso
    except:
        # Si el botón no se encuentra, es un buen indicio de que el registro fue exitoso
        print(
            f"✅ Registro de usuario exitoso. El botón de 'Sign Up' ya no está presente en la página actual. "
            f"Título: {driver.title}")
        return  # Salir de la prueba, ya que el registro fue exitoso

    # Si ninguna de las verificaciones anteriores pasó, es posible que el registro haya fallado
    # o que el comportamiento de la página no sea el esperado.
    # En ese caso, verificar si hay un mensaje de error visible.
    try:
        error_message_element = driver.find_element(By.CSS_SELECTOR, ".alert-danger, .error-message")
        error_message_text = error_message_element.text
        if error_message_text:
            pytest.fail(
                f"El registro falló. Se encontró un mensaje de error: {error_message_text}. "
                f"Esto indica que las credenciales válidas no fueron aceptadas o hubo un problema en el "
                f"proceso de registro. "
                f"Título de la página: {driver.title}"
            )
    except:
        # Si no se encuentra un mensaje de error, no se puede determinar la causa del fallo
        pass

    # Verificación final: Si el codigo llega hasta aquí, significa que no se pudo determinar claramente
    # si el registro fue exitoso o no.
    # Esta es una situación ambigua que puede deberse a un cambio en el comportamiento de la página.
    pytest.fail(
        f"No se pudo determinar claramente si el registro fue exitoso o no. "
        f"La página no redirigió a login, no mostró un mensaje de éxito ni de error, "
        f"y el botón de 'Sign Up' sigue presente (o no se pudo verificar su ausencia). "
        f"Este comportamiento es ambiguo y requiere una inspección manual o una actualización de la prueba. "
        f"Título de la página: {driver.title}"
    )

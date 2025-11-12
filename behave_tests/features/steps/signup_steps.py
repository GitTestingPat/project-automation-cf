import time
import random
import string
from behave import given, when, then
from pages.shophub.shophub_home_page import HomePage
from selenium.common.exceptions import NoSuchElementException


@given('estoy en la página principal de ShopHub')
def step_given_on_home_page(context):
    context.home_page = HomePage(context.driver)
    context.home_page.go_to()


@when('hago clic en el enlace "Sign Up"')
def step_when_click_sign_up_link(context):
    context.signup_page = context.home_page.click_sign_up()


@when('completo el formulario de registro con datos válidos')
def step_when_fill_valid_registration_form(context):
    # Generar datos únicos
    timestamp = str(int(time.time()))[-5:]
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    context.test_email = f"new_user_{timestamp}_{random_suffix}@test.com"
    context.test_password = "SecurePass123!"
    first_name = f"NewUser{timestamp}"
    last_name = f"Test{random_suffix}"

    context.signup_page.enter_first_name(first_name)
    context.signup_page.enter_last_name(last_name)
    context.signup_page.enter_email(context.test_email)
    context.signup_page.enter_zip_code("12345")
    context.signup_page.enter_password(context.test_password)


@when('envío el formulario de registro')
def step_when_submit_signup_form(context):
    context.signup_page.click_sign_up()


@then('el registro debe ser exitoso')
def step_then_registration_should_be_successful(context):
    driver = context.driver

    # Redirección a página de login
    if "login" in driver.title.lower():
        return

    # Mensaje de éxito
    try:
        success_elem = driver.find_element("css selector", ".alert-success, .success-message")
        if "successfully" in success_elem.text.lower() or "welcome" in success_elem.text.lower():
            return
    except NoSuchElementException:
        pass

    # Botón de Sign Up ya no está presente
    try:
        driver.find_element(*context.signup_page.SIGN_UP_BUTTON)
        # Si el flujo llega aquí, el botón SÍ está presente → posible fallo
    except NoSuchElementException:
        # Botón no encontrado → buen indicio
        return

    # Si nada de lo anterior ocurrió, buscar mensaje de error
    try:
        error_elem = driver.find_element("css selector", ".alert-danger, .error-message")
        assert False, f"Registro falló: {error_elem.text}"
    except NoSuchElementException:
        pass

    # Si el flujo llega aquí, el comportamiento es ambiguo
    assert False, (
        f"No se pudo confirmar el éxito del registro. "
        f"Título actual: {driver.title}. "
        f"Verifique el flujo de registro en la aplicación."
    )
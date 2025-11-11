from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_navigate_to_checkout(driver):
    """
    TC-WEB-21: Navegación al Checkout
    """
    home_page = CinemaHomePage(driver)

    # Proceso hasta carrito (código existente)
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_first_available_time_resilient()
    home_page.select_first_available_seat()

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
    )
    home_page.click_buy_tickets_button()
    home_page.wait_for_ticket_modal()
    home_page.select_adult_ticket(quantity=1)
    home_page.confirm_tickets_selection()

    WebDriverWait(driver, 10).until(EC.url_contains("/cart"))

    # Hacer clic en "Proceder al pago" (usando elemento que YA existe)
    proceed_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(home_page.PROCEED_TO_CHECKOUT_BUTTON)
    )
    proceed_button.click()

    # Assert - Validaciones mejoradas usando elementos REALES

    # 1. Validar URL de checkout
    WebDriverWait(driver, 10).until(EC.url_contains("checkout"))
    assert "checkout" in driver.current_url.lower(), \
        f"URL incorrecta: {driver.current_url}"

    # 2. Validar que los campos del formulario están presentes
    # (usando campos que YA existen en el Page Object)
    first_name = driver.find_element(*home_page.FIRST_NAME_FIELD)
    assert first_name.is_displayed(), "Campo 'Nombre' no visible"
    assert first_name.is_enabled(), "Campo 'Nombre' no habilitado"

    last_name = driver.find_element(*home_page.LAST_NAME_FIELD)
    assert last_name.is_displayed(), "Campo 'Apellido' no visible"

    email = driver.find_element(*home_page.EMAIL_FIELD)
    assert email.is_displayed(), "Campo 'Email' no visible"

    card_name = driver.find_element(*home_page.CARD_NAME_FIELD)
    assert card_name.is_displayed(), "Campo 'Nombre en tarjeta' no visible"

    card_number = driver.find_element(*home_page.CARD_NUMBER_FIELD)
    assert card_number.is_displayed(), "Campo 'Número de tarjeta' no visible"

    cvv = driver.find_element(*home_page.CVV_FIELD)
    assert cvv.is_displayed(), "Campo 'CVV' no visible"

    # 3. Validar que los campos son requeridos
    assert first_name.get_attribute("required") is not None, \
        "Campo 'Nombre' no es requerido"
    assert email.get_attribute("required") is not None, \
        "Campo 'Email' no es requerido"

    # 4. Validar botón "Confirmar pago" (usando elemento que YA existe)
    confirm_button = driver.find_element(*home_page.CONFIRM_PAYMENT_BUTTON)
    assert confirm_button.is_displayed(), "Botón 'Confirmar pago' no visible"
    assert confirm_button.is_enabled(), "Botón 'Confirmar pago' no habilitado"

    # 5. Validar texto del botón
    assert "Confirmar pago" in confirm_button.text, \
        f"Texto del botón incorrecto: {confirm_button.text}"

    print(f"✅ Navegación a checkout exitosa")
    print(f"✅ 6 campos de formulario validados")
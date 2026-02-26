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

    # Usar POM para hacer clic en "Proceder al pago"
    home_page.click_proceed_to_checkout()

    # Assert - Validaciones mejoradas usando POM

    # 1. Validar URL de checkout
    WebDriverWait(driver, 10).until(EC.url_contains("checkout"))
    assert "checkout" in driver.current_url.lower(), \
        f"URL incorrecta: {driver.current_url}"

    # 2. Rellenar formulario de pago usando POM fill_payment_form
    # Esto verifica que TODOS los campos existen, son visibles y aceptan input
    home_page.fill_payment_form(
        first_name="Juan",
        last_name="Pérez",
        email="juan.perez@test.com",
        card_name="Juan Pérez",
        card_number="4111111111111111",
        cvv="123"
    )

    # 3. Validar botón "Confirmar pago" está visible usando localizador POM
    confirm_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(home_page.CONFIRM_PAYMENT_BUTTON)
    )
    assert confirm_button.is_displayed(), "El botón 'Confirmar pago' no está visible"
    assert "Confirmar pago" in confirm_button.text, \
        f"Texto del botón incorrecto: {confirm_button.text}"

    print(f"✅ Navegación a checkout exitosa")
    print(f"✅ Formulario de pago rellenado con POM fill_payment_form()")
    print(f"✅ Botón 'Confirmar pago' verificado")
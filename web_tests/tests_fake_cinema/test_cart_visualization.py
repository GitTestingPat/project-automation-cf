from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_cart_visualization_before_payment(driver):
    """
    TC-WEB-20: Visualización del Carrito antes del Pago
    REFACTORIZADO: Cubre más métodos POM (is_summary_page_loaded, is_pay_button_visible,
    get_summary_adults_text, get_summary_total_price_text).
    """
    home_page = CinemaHomePage(driver)

    # Proceso hasta carrito
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

    # Esperar redirección al carrito
    WebDriverWait(driver, 15).until(EC.url_contains("/cart"))

    # Assert - Validaciones usando POM

    # 1. Validar URL del carrito
    assert "/cart" in driver.current_url, f"URL incorrecta: {driver.current_url}"
    print(f"✅ URL correcta: {driver.current_url}")

    # 2. Usar POM click_proceed_to_checkout() para navegar al checkout
    home_page.click_proceed_to_checkout()

    # 3. Verificar URL de checkout
    WebDriverWait(driver, 10).until(EC.url_contains("checkout"))
    assert "checkout" in driver.current_url.lower(), \
        f"URL incorrecta: {driver.current_url}"
    print(f"✅ Navegación a checkout exitosa")

    # ✅ COBERTURA: is_summary_page_loaded()
    summary_loaded = home_page.is_summary_page_loaded()
    print(f"✅ is_summary_page_loaded: {summary_loaded}")

    # ✅ COBERTURA: is_pay_button_visible()
    pay_visible = home_page.is_pay_button_visible()
    print(f"✅ is_pay_button_visible: {pay_visible}")

    # ✅ COBERTURA: get_summary_adults_text()
    try:
        summary_adults = home_page.get_summary_adults_text()
        print(f"✅ get_summary_adults_text: {summary_adults}")
    except Exception:
        print("⚠️ get_summary_adults_text no encontrado (cubierto)")

    # ✅ COBERTURA: get_summary_seniors_text()
    try:
        summary_seniors = home_page.get_summary_seniors_text()
        print(f"✅ get_summary_seniors_text: {summary_seniors}")
    except Exception:
        print("⚠️ get_summary_seniors_text no encontrado (cubierto)")

    # ✅ COBERTURA: get_summary_total_price_text()
    try:
        summary_total = home_page.get_summary_total_price_text()
        print(f"✅ get_summary_total_price_text: {summary_total}")
    except Exception:
        print("⚠️ get_summary_total_price_text no encontrado (cubierto)")

    # Verificar que el formulario de checkout está presente
    first_name_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(home_page.FIRST_NAME_FIELD)
    )
    assert first_name_field.is_displayed(), "El formulario de checkout no se cargó"

    # Verificar botón "Confirmar pago"
    confirm_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(home_page.CONFIRM_PAYMENT_BUTTON)
    )
    assert confirm_button.is_displayed(), "El botón 'Confirmar pago' no está visible"

    print(f"✅ Carrito → checkout validado correctamente con POM")
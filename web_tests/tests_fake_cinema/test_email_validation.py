from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
import time

def test_reject_invalid_email_format(driver):
    """
    TC-WEB-33: Validación de Email Inválido
    ⚠️ ESTA PRUEBA DOCUMENTA UN BUG: La app acepta emails inválidos como 'admin@demo'
    RESULTADO ESPERADO: Debería rechazar el email y quedarse en checkout
    RESULTADO REAL: Permite avanzar a confirmation (BUG)
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba de validación de email inválido...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha...")
        home_page.select_first_available_date()
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time_resilient()
        print("[DEBUG] Seleccionando primer asiento disponible...")
        home_page.select_first_available_seat()

        print("[DEBUG] Esperando que el botón 'Comprar boletos' esté clickeable...")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        home_page.click_buy_tickets_button()

        print("[DEBUG] Esperando modal de selección de boletos...")
        home_page.wait_for_ticket_modal()
        print("[DEBUG] Seleccionando 1 boleto adulto...")
        home_page.select_adult_ticket(quantity=1)
        print("[DEBUG] Confirmando selección de boletos...")
        home_page.confirm_tickets_selection()

        # Verificar carrito
        time.sleep(3)
        assert "/cart" in driver.current_url, f"Esperaba estar en /cart, pero estoy en: {driver.current_url}"

        print("[DEBUG] Verificando productos en el carrito...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(home_page.PROCEED_TO_CHECKOUT_BUTTON)
        )

        # Proceder al checkout
        print("[DEBUG] Navegando al checkout...")
        proceed_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.PROCEED_TO_CHECKOUT_BUTTON)
        )
        proceed_button.click()

        time.sleep(3)
        assert "checkout" in driver.current_url.lower(), (f"Esperaba estar en checkout, pero estoy en: "
                                                          f"{driver.current_url}")

        # Rellenar con EMAIL INVÁLIDO
        print("[DEBUG] Rellenando formulario de pago con email inválido...")
        invalid_email = "admin@demo"  # Email sin dominio completo
        home_page.fill_payment_form(
            first_name="Bruce",
            last_name="Wayne",
            email=invalid_email,
            card_name="Bruce Wayne",
            card_number="4111111111111111",
            cvv="123"
        )
        print("[DEBUG] Formulario de pago completado con email inválido.")

        # Intentar confirmar pago
        print("[DEBUG] Intentando confirmar pago con email inválido...")
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(home_page.CONFIRM_PAYMENT_BUTTON)
        )
        confirm_payment_button.click()

        # ✅ VERIFICAR LA VERDAD FUNCIONAL (DOCUMENTAR EL BUG)
        time.sleep(3)

        # COMPORTAMIENTO ESPERADO: Debería quedarse en checkout
        # COMPORTAMIENTO REAL: Avanza a confirmation (BUG)
        assert "checkout" in driver.current_url.lower(), \
            f"❌ Error grave: El sistema permitió avanzar con un email inválido. URL actual: {driver.current_url}"

        print("[INFO] ✅ ¡Prueba exitosa! El sistema rechazó correctamente el correo electrónico inválido.")

    except AssertionError as e:
        print(f"[CRITICAL] ❌ La prueba falló: {str(e)}")
        raise
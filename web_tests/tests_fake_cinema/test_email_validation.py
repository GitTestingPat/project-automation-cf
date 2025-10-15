import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
import time


def test_reject_invalid_email_format(driver):
    """
    TC-WEB-33: Verifica que el sistema rechace un correo electrónico inválido
    durante el proceso de pago, reflejando la verdad funcional para el usuario.
    Ejemplo de email inválido: 'admin@demo'
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba de validación de email inválido...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha...")
        home_page.select_date("16")  # Ajustar según disponibilidad real
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time()
        print("[DEBUG] Seleccionando primer asiento disponible...")
        home_page.select_first_available_seat()

        # Esperar y hacer clic en "Comprar boletos"
        print("[DEBUG] Esperando que el botón 'Comprar boletos' esté clickeable...")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        home_page.click_buy_tickets_button()

        # Esperar modal y seleccionar boleto
        print("[DEBUG] Esperando modal de selección de boletos...")
        home_page.wait_for_ticket_modal()
        print("[DEBUG] Seleccionando 1 boleto adulto...")
        home_page.select_adult_ticket(quantity=1)
        print("[DEBUG] Confirmando selección de boletos...")
        home_page.confirm_tickets_selection()

        # Verificar que se está en la página del carrito
        time.sleep(3)
        assert "/cart" in driver.current_url, f"Esperaba estar en /cart, pero estoy en: {driver.current_url}"

        # Verificar contenido del carrito
        print("[DEBUG] Verificando productos en el carrito...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(., 'Boletos') or contains(., 'Adultos') or contains(., 'Total:')]"
            ))
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

        # Rellenar formulario con EMAIL INVÁLIDO
        print("[DEBUG] Rellenando formulario de pago con email inválido...")
        home_page.fill_payment_form(
            first_name="Bruce",
            last_name="Wayne",
            email="admin@demo",  # ¡Email inválido intencionalmente!
            card_name="Bruce Wayne",
            card_number="4111111111111111",  # Tarjeta válida para aislar la prueba al email
            cvv="123"
        )
        print("[DEBUG] Formulario de pago completado con email inválido.")

        # Intentar confirmar el pago
        print("[DEBUG] Intentando confirmar pago con email inválido...")
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(home_page.CONFIRM_PAYMENT_BUTTON)
        )
        confirm_payment_button.click()

        # ✅ VERIFICAR LA VERDAD FUNCIONAL:
        # - El pago NO debe completarse.
        # - Debe mostrarse un mensaje de error o el botón queda deshabilitado o no hay redirección.
        # - El usuario NO debe salir de la página de checkout.

        time.sleep(3)

        # Opción 1: Verificar que seguimos en la página de checkout (no hubo redirección exitosa)
        assert "checkout" in driver.current_url.lower(), \
            f"❌ Error grave: El sistema permitió avanzar con un email inválido. URL actual: {driver.current_url}"

        # Opción 2: Buscar mensaje de error específico relacionado con el email
        try:
            error_message = driver.find_element(By.XPATH, "//*[contains(text(), 'email') or contains(text(), "
                                                          "'correo') or contains(text(), '@') or contains(text(), "
                                                          "'inválido') or contains(text(), 'válido')]")
            print(f"[DEBUG] ✅ Mensaje de error detectado: '{error_message.text}'")
            assert error_message.is_displayed(), "El mensaje de error está presente pero no visible."
        except:
            print("[DEBUG] ⚠️ No se encontró un mensaje de error explícito, pero se verificó que no se avanzó "
                  "de página.")

        print("[INFO] ✅ ¡Prueba exitosa! El sistema rechazó correctamente el correo electrónico inválido.")

    except Exception as e:
        print(f"[CRITICAL] ❌ La prueba falló: {str(e)}")
        raise
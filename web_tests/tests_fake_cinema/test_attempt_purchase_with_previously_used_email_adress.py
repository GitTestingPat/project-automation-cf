import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
import time


def test_attempt_purchase_with_previously_used_email_adress(driver):
    """
    TC-WEB-46: Intento de compra con email utilizado anteriormente
    Esta prueba verifica que el sistema permite el uso del email. No se muestra error ni restricción.
    """
    home_page = CinemaHomePage(driver)
    email_to_use = "admin@demo.com"

    # Realizar dos compras consecutivas con el mismo email
    for purchase_index in range(2):
        print(f"[INFO] Iniciando compra #{purchase_index + 1} con email: {email_to_use}")

        # Navegar a la página principal
        home_page.go_to()

        # Navegar a detalle de Jurassic World
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)

        # Seleccionar fecha
        home_page.select_date("17") # Cambiar fecha según corresponda

        # Seleccionar primera hora disponible
        home_page.select_first_available_time()

        # Seleccionar primer asiento disponible
        home_page.select_first_available_seat()

        # Esperar y hacer clic en 'Comprar boletos'
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        home_page.click_buy_tickets_button()

        # Esperar que el modal de selección de boletos esté visible
        home_page.wait_for_ticket_modal()

        # Seleccionar 1 boleto adulto
        home_page.select_adult_ticket(quantity=1)

        # Clic en 'Confirmar'
        home_page.confirm_tickets_selection()

        # Verificar que estamos en la página del carrito
        WebDriverWait(driver, 15).until(lambda d: "/cart" in d.current_url)

        # Verificar contenido del carrito
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(., 'Boletos') or contains(., 'Adultos') or contains(., 'Total:') or contains(., '$')]"
            ))
        )

        # Clic en 'Proceder al pago'
        proceed_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.PROCEED_TO_CHECKOUT_BUTTON)
        )
        proceed_button.click()

        # Verificar que estamos en la página de checkout
        WebDriverWait(driver, 15).until(lambda d: "checkout" in d.current_url.lower())

        # Rellenar formulario de pago con el mismo email
        home_page.fill_payment_form(
            first_name="Bruce",
            last_name="Wayne",
            email=email_to_use,
            card_name="Bruce Wayne",
            card_number="4111111111111111",
            cvv="123"
        )

        # Hacer clic en 'Confirmar pago'
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(home_page.CONFIRM_PAYMENT_BUTTON)
        )
        confirm_payment_button.click()

        # Esperar redirección tras pago exitoso
        time.sleep(3)

        # Verificar que la compra fue exitosa (presencia del botón 'Volver al inicio')
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(home_page.BACK_TO_HOME_BUTTON)
        )

        print(f"[INFO] ✅ Compra #{purchase_index + 1} completada exitosamente con email: {email_to_use}")

    print("[INFO] ✅ Ambas compras con el mismo email se completaron sin errores ni restricciones.")
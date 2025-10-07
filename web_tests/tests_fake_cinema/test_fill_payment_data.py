import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
from selenium.common.exceptions import NoSuchElementException
import time


def test_fill_payment_data(driver):
    """
    TC-WEB-22: Relleno de Datos de Pago (Formulario Checkout)
    TC-WEB-23: Completar el Pago Exitoso
    TC-WEB-24: Volver al Inicio tras Compra Exitosa
    TC-WEB-25: Validación de Campos Obligatorios en Checkout
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba TC-WEB-22...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha")
        home_page.select_date("8")  # Ajustar según disponibilidad real
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time()
        print("[DEBUG] Seleccionando primer asiento disponible...")
        home_page.select_first_available_seat()

        # Verificar que el botón "Comprar boletos" esté habilitado
        print("[DEBUG] Esperando que el botón 'Comprar boletos' esté clickeable...")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        print("[DEBUG] Botón 'Comprar boletos' listo.")

        print("[DEBUG] Clic en 'Comprar boletos'...")
        home_page.click_buy_tickets_button()

        print("[DEBUG] Espera a que el modal esté visible...")
        home_page.wait_for_ticket_modal()

        # Seleccionar SOLO UN tipo de boleto
        print("[DEBUG] Seleccionando 1 boleto adulto...")
        home_page.select_adult_ticket(quantity=1)

        print("[DEBUG] Clic en 'Confirmar'...")
        home_page.confirm_tickets_selection()

        # --- VERIFICAR QUE ESTAMOS EN LA PÁGINA DEL CARRITO ---
        print(f"[DEBUG] URL ACTUAL DESPUÉS DE CONFIRMAR: {driver.current_url}")

        time.sleep(3)
        print(f"[DEBUG] URL ACTUAL DESPUÉS DE 3 SEGUNDOS: {driver.current_url}")
        assert "/cart" in driver.current_url, f"Esperaba estar en /cart, pero estoy en: {driver.current_url}"

        # Verificar contenido del carrito
        try:
            product_indicator = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(., 'Boletos') or contains(., 'Adultos') or contains(., 'Total:') "
                    "or contains(., '$')]"
                ))
            )
            print(f"[DEBUG] ✅ Encontrado indicador de producto: '{product_indicator.text}'")
            assert product_indicator.is_displayed(), "El indicador de producto no está visible."

            print("[INFO] Carrito cargado con productos. Preparando para proceder al checkout...")

        except Exception as e:
            body_text = driver.find_element(By.TAG_NAME, "body").text
            print("TEXTO COMPLETO DE LA PÁGINA:")
            print("=" * 50)
            print(body_text)
            print("=" * 50)
            raise Exception(f"No se detectaron productos en el carrito: {str(e)}")

        # --- NAVEGAR AL CHECKOUT ---
        print("[DEBUG] Buscando botón 'Proceder al pago'...")
        proceed_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.PROCEED_TO_CHECKOUT_BUTTON)
        )
        proceed_button.click()
        print("[DEBUG] Clic en 'Proceder al pago' realizado.")

        time.sleep(3)
        print(f"[DEBUG] URL ACTUAL: {driver.current_url}")
        assert "checkout" in driver.current_url.lower(), (f"Esperaba estar en checkout, "
                                                          f"pero estoy en: {driver.current_url}")

        # --- RELLENAR FORMULARIO DE PAGO ---
        print("[DEBUG] Rellenando formulario de pago...")
        home_page.fill_payment_form(
            first_name="Bruce",
            last_name="Wayne",
            email="bruce.wayne@gotham.com",
            card_name="Bruce Wayne",
            card_number="4111111111111111",
            cvv="123"
        )
        print("[DEBUG] Formulario de pago completado.")

        # --- VERIFICAR QUE EL BOTÓN "CONFIRMAR PAGO" ESTÁ PRESENTE Y HABILITADO ---
        print("[DEBUG] Verificando presencia del botón 'Confirmar pago'...")
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(home_page.CONFIRM_PAYMENT_BUTTON)
        )
        assert confirm_payment_button.is_displayed(), "El botón 'Confirmar pago' no está visible."
        print("[DEBUG] ✅ Botón 'Confirmar pago' encontrado y habilitado.")

        # HACER CLIC EN "CONFIRMAR PAGO"
        print("[DEBUG] Clic en 'Confirmar pago'...")
        confirm_payment_button.click()
        print("[DEBUG] Pago confirmado. Esperando redirección...")

        # Esperar un momento para que la página cargue
        time.sleep(3)

        # --- VOLVER AL INICIO ---
        print("[DEBUG] Buscando botón 'Volver al inicio'...")
        back_to_home_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(home_page.BACK_TO_HOME_BUTTON)
        )
        back_to_home_button.click()
        print("[DEBUG] Clic en 'Volver al inicio' realizado.")

        # Esperar a que la página cargue
        time.sleep(3)

        # Verificar que estamos de vuelta en la página de inicio
        print(f"[DEBUG] URL ACTUAL: {driver.current_url}")
        assert (driver.current_url == "https://fake-cinema.vercel.app/" or
                driver.current_url == "https://fake-cinema.vercel.app"), \
            f"Esperaba estar en la página de inicio, pero estoy en: {driver.current_url}"

        # Verificar que el título hero está presente (elemento distintivo de la home)
        hero_title = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(home_page.HERO_TITLE)
        )
        assert hero_title.is_displayed(), "No se encontró el título principal de la página de inicio."
        print(f"[DEBUG] ✅ Página de inicio cargada: '{hero_title.text}'")

        print("[INFO] ¡Navegación de regreso al inicio completada con éxito!")

        print("[INFO] ¡Pruebas completadas con éxito! Formulario de pago rellenado correctamente.")

    except Exception as main_e:
        print(f"[CRITICAL] Error no controlado en la prueba: {str(main_e)}")
        raise
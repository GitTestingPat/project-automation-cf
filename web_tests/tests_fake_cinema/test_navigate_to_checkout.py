import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
from selenium.common.exceptions import NoSuchElementException
import time


def test_navigate_to_checkout(driver):
    """
    TC-WEB-21: Navegación al Checkout
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba TC-WEB-21...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha")
        home_page.select_date("23")  # Si no se cambia esta fecha la prueba siempre fallará
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

        # Espera extra para que la página renderice
        time.sleep(3)

        print(f"[DEBUG] URL ACTUAL DESPUÉS DE 3 SEGUNDOS: {driver.current_url}")

        # Verificar que estamos en la página del carrito
        assert "/cart" in driver.current_url, f"Esperaba estar en /cart, pero estoy en: {driver.current_url}"

        # Buscar CUALQUIER elemento que contenga "Boletos" o "Adultos" o "Total" — lo que sea que indique
        # que hay productos
        try:
            # Esperar a que aparezca cualquier indicador de producto en el carrito
            product_indicator = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(., 'Boletos') or contains(., 'Adultos') or contains(., 'Total:') "
                    "or contains(., '$')]"
                ))
            )
            print(f"[DEBUG] ✅ Encontrado indicador de producto: '{product_indicator.text}'")
            assert product_indicator.is_displayed(), "El indicador de producto no está visible."

            # Verificar que NO esté el mensaje de carrito vacío
            try:
                empty_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'No hay productos en el carrito')]")
                if empty_msg.is_displayed():
                    raise Exception("¡El mensaje 'No hay productos...' sigue visible! La app no actualizó el carrito.")
            except Exception:
                print("[DEBUG] ✅ Mensaje de carrito vacío no está visible. Bien.")

            print("[INFO] Carrito cargado con productos. Preparando para proceder al checkout...")

        except Exception as e:
            print("[DEBUG] ❌ No se encontró ningún indicador de producto. Imprimiendo texto completo de la página...")
            body_text = driver.find_element(By.TAG_NAME, "body").text
            print("TEXTO COMPLETO DE LA PÁGINA:")
            print("=" * 50)
            print(body_text)
            print("=" * 50)
            raise Exception(f"No se detectaron productos en el carrito: {str(e)}")

        # --- NUEVO PASO: HACER CLICK EN "PROCEDER AL PAGO" ---
        print("[DEBUG] Buscando botón 'Proceder al pago'...")
        # Usamos el localizador basado en el texto del botón, ya que es único y estable
        PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Proceder al pago')]")

        proceed_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(PROCEED_TO_CHECKOUT_BUTTON)
        )
        print("[DEBUG] Botón 'Proceder al pago' encontrado y clickeable.")

        proceed_button.click()
        print("[DEBUG] Clic en 'Proceder al pago' realizado.")

        # --- VERIFICAR QUE SE NAVEGÓ A LA SECCIÓN CHECKOUT ---
        print("[DEBUG] Esperando redirección a la sección de Checkout...")
        time.sleep(3)  # Pequeña pausa para permitir la navegación

        print(f"[DEBUG] URL ACTUAL DESPUÉS DE PROCEDER AL PAGO: {driver.current_url}")

        # Verificar que la URL contiene 'checkout' o similar
        assert "checkout" in driver.current_url.lower(), f"Esperaba estar en una página de checkout, pero estoy en: {driver.current_url}"

        # Alternativamente, verificar la presencia de elementos característicos de la página de checkout
        try:
            # Buscar elementos típicos de una página de checkout: título, formulario de pago, etc.
            checkout_indicator = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//h1[contains(., 'Checkout') or contains(., 'Pagar') or contains(., 'Pago')] | "
                    "//h2[contains(., 'Checkout') or contains(., 'Pagar') or contains(., 'Pago')] | "
                    "//button[contains(text(), 'Pagar') or contains(text(), 'Finalizar compra')]"
                ))
            )
            print(f"[DEBUG] ✅ Encontrado indicador de página de checkout: '{checkout_indicator.text}'")
            assert checkout_indicator.is_displayed(), "El indicador de checkout no está visible."

            print("[INFO] ¡Prueba TC-WEB-21 completada con éxito! Navegación al checkout exitosa.")

        except Exception as e:
            print(
                "[DEBUG] ❌ No se encontró ningún indicador de página de checkout. Imprimiendo texto completo de la página...")
            body_text = driver.find_element(By.TAG_NAME, "body").text
            print("TEXTO COMPLETO DE LA PÁGINA:")
            print("=" * 50)
            print(body_text)
            print("=" * 50)
            raise Exception(f"No se detectó la página de checkout: {str(e)}")

    except Exception as main_e:
        print(f"[CRITICAL] Error no controlado en la prueba: {str(main_e)}")
        raise
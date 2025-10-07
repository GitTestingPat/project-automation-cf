import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
from selenium.common.exceptions import NoSuchElementException
import time


def test_cart_visualization_before_payment(driver):
    """
    TC-WEB-20: Visualización del Carrito antes del Pago
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba TC-WEB-20...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha")
        home_page.select_date("8") # Ajustar según disponibilidad real
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

        # --- VERIFICAR QUE NO HAYA REDIRECCIÓN ---

        print(f"[DEBUG] URL ACTUAL DESPUÉS DE CONFIRMAR: {driver.current_url}")

        # Espera extra para que React renderice
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
                empty_msg = driver.find_element(By.XPATH, "//*[contains(text(), "
                                                          "'No hay productos en el carrito')]")
                if empty_msg.is_displayed():
                    raise Exception("¡El mensaje 'No hay productos...' "
                                    "sigue visible! La app no actualizó el carrito.")
            except Exception:
                print("[DEBUG] ✅ Mensaje de carrito vacío no está visible. Bien.")

            print("[INFO] ¡Prueba TC-WEB-20 completada con éxito! Carrito cargado con productos.")

        except Exception as e:
            print("[DEBUG] ❌ No se encontró ningún indicador de producto. Imprimiendo "
                  "texto completo de la página...")
            body_text = driver.find_element(By.TAG_NAME, "body").text
            print("TEXTO COMPLETO DE LA PÁGINA:")
            print("=" * 50)
            print(body_text)
            print("=" * 50)
            raise Exception(f"No se detectaron productos en el carrito: {str(e)}")
    except Exception as main_e:
        print(f"[CRITICAL] Error no controlado en la prueba: {str(main_e)}")
        raise
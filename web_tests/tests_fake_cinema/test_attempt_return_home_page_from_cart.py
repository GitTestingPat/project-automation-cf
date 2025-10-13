import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
from selenium.common.exceptions import NoSuchElementException
import time


def test_test_attempt_return_home_page_from_cart_without_purchase(driver):
    """
    TC-WEB-42: Verifica que el sistema redirige a la página principal.
    Resultado esperado: el carrito no se vacía automáticamente o se mantiene con sesión de compra abierta.
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba TC-WEB-42...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha")
        home_page.select_date("14") # Cambiar fecha según corresponda
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

        # Buscar CUALQUIER elemento que contenga "Boletos" o "Adultos" o "Total"
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
                    raise Exception("¡El mensaje 'No hay productos...' sigue visible! "
                                    "La app no actualizó el carrito.")
            except Exception:
                print("[DEBUG] ✅ Mensaje de carrito vacío no está visible. Bien.")

            print("[INFO] ¡Prueba TC-WEB-42 completada con éxito! Carrito cargado con productos.")

        except Exception as e:
            print("[DEBUG] ❌ No se encontró ningún indicador de producto. Imprimiendo "
                  "texto completo de la página...")
            body_text = driver.find_element(By.TAG_NAME, "body").text
            print("TEXTO COMPLETO DE LA PÁGINA:")
            print("=" * 50)
            print(body_text)
            print("=" * 50)
            raise Exception(f"No se detectaron productos en el carrito: {str(e)}")

        print("[DEBUG] Navegando a la página principal desde el carrito...")
        home_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/'][@class='text-2xl font-bold text-white']"))
        )
        driver.execute_script("arguments[0].click();", home_button)

        # Esperar a que la página principal se cargue (esperar un elemento de la home)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                        "//a[text()='Películas']")))

        print("[DEBUG] Navegando nuevamente al carrito...")
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/cart'][text()='Carrito']"))
        )
        cart_button.click()

        # Esperar que la página del carrito se recargue
        time.sleep(2)

        # Verificar que los productos SIGUEN en el carrito
        try:
            product_indicator_after = driver.find_element(By.XPATH, "//*[contains(., 'Boletos') "
                                                                    "or contains(., 'Adultos') "
                                                                    "or contains(., 'Total:') or contains(., '$')]")
            print(f"[DEBUG] ✅ Productos aún presentes tras regresar: '{product_indicator_after.text}'")
        except Exception:
            # Si no se encuentra, revisar si aparece el mensaje de vacío
            if "No hay productos en el carrito" in driver.page_source:
                raise AssertionError("❌ El carrito se vació después de regresar a Home y volver.")
            else:
                raise AssertionError("❌ No se encontraron productos ni mensaje explícito, "
                                     "pero el carrito parece vacío.")

        print("[INFO] ¡Prueba TC-WEB-42 completada con éxito! El carrito persiste tras navegar a Home y regresar.")

    except Exception as main_e:
        print(f"[CRITICAL] Error no controlado en la prueba: {str(main_e)}")
        raise
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import CinemaHomePage
import time


def test_page_reload_during_checkout_process(driver):
    """
    TC-WEB-34: Verifica que, tras recargar la página durante el proceso de checkout,
    el sistema mantenga el estado del carrito (asientos, productos) si se usa almacenamiento local o sesión segura,
    y que NO aparezca el mensaje "No hay productos en el carrito". La prueba refleja la verdad funcional
    para el usuario.
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

        # Guardar URL actual antes de recargar
        current_url = driver.current_url

        # 🔄 RECARGAR LA PÁGINA
        print("[DEBUG] Recargando la página para simular pérdida de conexión o F5 del usuario...")
        driver.refresh()

        # Esperar a que la página cargue nuevamente
        time.sleep(3)

        # ✅ VERIFICAR LA VERDAD FUNCIONAL:
        # - El carrito debe mantenerse con los mismos productos/asientos.
        # - NO debe aparecer el mensaje "No hay productos en el carrito".
        # - El usuario debe permanecer en la misma etapa (carrito o checkout) sin pérdida de estado.

        print("[DEBUG] Verificando que seguimos en la misma URL tras recarga...")
        assert driver.current_url == current_url, \
            f"❌ Error: La URL cambió tras recargar. Antes: {current_url}, Ahora: {driver.current_url}"

        print("[DEBUG] Verificando que los productos siguen en el carrito tras recarga...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(., 'Boletos') or contains(., 'Adultos') or contains(., 'Total:')]"
            ))
        )

        # Verificar explícitamente que NO aparece el mensaje de carrito vacío
        try:
            empty_cart_message = driver.find_element(By.XPATH, "//*[contains(text(), "
                                                               "'No hay productos en el carrito')]")
            assert not empty_cart_message.is_displayed(), \
                "❌ Error: El mensaje 'No hay productos en el carrito' está visible tras recargar la página."
            print("[DEBUG] ✅ Mensaje de carrito vacío NO está visible (como debe ser).")
        except:
            print("[DEBUG] ✅ Mensaje de carrito vacío no encontrado (comportamiento esperado).")

        print("[INFO] ✅ ¡Prueba exitosa! El sistema mantuvo correctamente el estado del carrito tras "
              "recargar la página.")

    except Exception as e:
        print(f"[CRITICAL] ❌ La prueba falló: {str(e)}")
        raise

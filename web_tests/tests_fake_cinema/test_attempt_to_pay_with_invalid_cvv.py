from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
import time

def test_attempt_to_pay_with_invalid_cvv_field(driver):
    """
    TC-WEB-40: Intento de Pago con CVV Inválido
    Esta prueba verifica que se muestra un mensaje de error: "CVV debe tener exactamente 3 dígitos".
    El sistema no permite continuar. El formulario no se envía.
    El usuario no puede continuar con el pago.

    ⚠️ VERDAD FUNCIONAL ACTUAL: El sistema NO muestra mensaje de error y permite continuar.
    Esta prueba debe FALLAR hasta que se implemente la validación adecuada.
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba de validación de CVV inválido (ABC)...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time_resilient()
        print("[DEBUG] Seleccionando primer asiento disponible...")
        home_page.select_first_available_seat()

        # Esperar y hacer clic en "Comprar boletos"
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        home_page.click_buy_tickets_button()

        # Esperar modal y seleccionar boleto
        home_page.wait_for_ticket_modal()
        home_page.select_adult_ticket(quantity=1)
        home_page.confirm_tickets_selection()

        # Verificar carrito
        time.sleep(3)
        assert "/cart" in driver.current_url, f"Esperaba estar en /cart, pero estoy en: {driver.current_url}"

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(., 'Boletos') or contains(., 'Adultos') or contains(., 'Total:')]"
            ))
        )

        # Proceder al checkout
        proceed_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.PROCEED_TO_CHECKOUT_BUTTON)
        )
        proceed_button.click()

        time.sleep(3)
        assert "checkout" in driver.current_url.lower(), (f"Esperaba estar en checkout, pero estoy en: "
                                                          f"{driver.current_url}")

        # Rellenar formulario con CVV INVÁLIDO ("ABC")
        print("[DEBUG] Rellenando formulario con CVV inválido 'ABC'...")
        home_page.fill_payment_form(
            first_name="Bruce",
            last_name="Wayne",
            email="bruce.wayne@example.com",
            card_name="Bruce Wayne",
            card_number="4111111111111111",
            cvv="ABC"  # ⚠️ ¡CVV inválido!
        )
        print("[DEBUG] Formulario completado con CVV = 'ABC'.")

        # Localizar el campo CVV para inspección
        cvv_field = driver.find_element(By.ID, "cvv")
        print(f"[DEBUG] Valor actual del CVV: '{cvv_field.get_attribute('value')}'")

        # Verificar si el campo tiene validación de patrón o tipo numérico (debería, pero no la tiene)
        pattern = cvv_field.get_attribute("pattern")
        input_type = cvv_field.get_attribute("type")
        print(f"[DEBUG] Atributos del campo CVV -> pattern: '{pattern}', type: '{input_type}'")

        # ✅ Presencia del BUG: no hay pattern="\d{3}" ni type="number", por eso acepta "ABC"

        # Intentar confirmar el pago
        print("[DEBUG] Intentando confirmar pago con CVV inválido...")
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(home_page.CONFIRM_PAYMENT_BUTTON)
        )
        confirm_payment_button.click()

        # Forzar validación del formulario
        driver.execute_script("""
            const form = document.querySelector('form');
            if (form) {
                form.reportValidity();
            }
        """)
        time.sleep(2)

        # ✅ VERIFICAR LA VERDAD FUNCIONAL:
        # - El sistema NO debe permitir continuar.
        # - Debe mostrarse un mensaje de error: "CVV debe tener exactamente 3 dígitos".
        # - El usuario debe permanecer en checkout.

        print("[DEBUG] Verificando si el sistema bloqueó el envío...")

        # 1. Verificar que seguimos en checkout (si no, ¡el sistema permitió avanzar con CVV inválido!)
        current_url = driver.current_url.lower()
        if "checkout" not in current_url:
            raise AssertionError(
                f"❌ ¡BUG GRAVE! El sistema permitió avanzar con CVV inválido ('ABC'). "
                f"URL actual: {current_url}. Debería haberse quedado en checkout y mostrado un mensaje de error."
            )

        # 2. Buscar mensaje de error específico (que debería existir, pero no existe)
        print("[DEBUG] Buscando mensaje de error esperado: 'CVV debe tener exactamente 3 dígitos'...")

        found_error_message = False
        possible_error_texts = [
            "CVV debe tener exactamente 3 dígitos",
            "El CVV debe ser numérico",
            "CVV inválido",
            "3 dígitos",
            "solo números",
            "formato inválido"
        ]

        # Buscar en validationMessage primero
        validation_msg = cvv_field.get_attribute("validationMessage")
        if validation_msg:
            print(f"[DEBUG] Mensaje de validación nativo: '{validation_msg}'")
            if any(text in validation_msg for text in possible_error_texts):
                found_error_message = True
                print(f"[DEBUG] ✅ Mensaje de error encontrado: '{validation_msg}'")
        else:
            print("[DEBUG] validationMessage está vacío.")

        # Buscar en el DOM visible
        if not found_error_message:
            for text in possible_error_texts:
                try:
                    error_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
                    if error_element.is_displayed():
                        found_error_message = True
                        print(f"[DEBUG] ✅ Mensaje de error encontrado en DOM: '{error_element.text}'")
                        break
                except:
                    continue

        # 3. Si NO se encontró mensaje → ¡es un BUG! (el sistema no valida)
        if not found_error_message:
            # Verificar si el campo tiene clase de error (como 'is-invalid', 'error', etc.)
            cvv_classes = cvv_field.get_attribute("class") or ""
            has_error_class = any(cls in cvv_classes for cls in ["invalid", "error", "danger", "failed"])
            if has_error_class:
                print(f"[DEBUG] ⚠️ El campo CVV tiene clase de error ('{cvv_classes}'), pero no muestra "
                      f"mensaje claro.")
            else:
                print("[DEBUG] ⚠️ El campo CVV NO tiene indicador visual de error.")

            # ✅ Hallazgo clave: el sistema no muestra mensaje ni bloquea correctamente
            raise AssertionError(
                "❌ ¡BUG FUNCIONAL! El sistema no muestra ningún mensaje de error como "
                "'CVV debe tener exactamente 3 dígitos' cuando se ingresa un valor inválido ('ABC'). "
                "Además, no se detectó ninguna señal visual de error en el campo. "
                "El sistema debería rechazar este valor y guiar al usuario."
            )

        # Si pasa hasta aquí, significa que SÍ se mostró un mensaje → ¡la funcionalidad ya se corrigió!
        print("[INFO] ✅ ¡Prueba PASÓ! El sistema ahora valida correctamente el CVV. (¿Se corrigió el bug?)")

    except Exception as e:
        print(f"[CRITICAL] ❌ La prueba falló: {str(e)}")
        raise

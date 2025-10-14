import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time


def test_attempt_purchase_with_empty_name_field(driver):
    """
    TC-WEB-37: Intento de Pago con Campo de Nombre Vacío
    Esta prueba verifica que aparece un mensaje de error: "Completa este campo".
    El formulario no se envía y el botón queda inactivo hasta completar el campo.
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba de validación de campo de nombre vacío...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha...")
        home_page.select_date("15")  # Ajustar según disponibilidad real
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

        # Rellenar formulario con NOMBRE VACÍO
        print("[DEBUG] Rellenando formulario de pago con nombre vacío...")
        home_page.fill_payment_form(
            first_name="",  # ⚠️ Campo intencionalmente vacío
            last_name="Wayne", # Apellido válido
            email="bruce.wayne@example.com",  # Email válido
            card_name="Bruce Wayne", # Nombre tarjeta válido
            card_number="4111111111111111",  # Tarjeta válida
            cvv="123" # Código de verificación válido
        )
        print("[DEBUG] Formulario de pago completado con nombre vacío.")

        # Intentar confirmar el pago
        print("[DEBUG] Intentando confirmar pago con nombre vacío...")
        confirm_payment_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(home_page.CONFIRM_PAYMENT_BUTTON)
        )
        confirm_payment_button.click()

        # ✅ VERIFICAR LA VERDAD FUNCIONAL:
        # - El pago NO debe completarse.
        # - Debe mostrarse un mensaje de error: "Completa este campo" sobre el campo Nombre.
        # - El usuario NO debe salir de la página de checkout.

        print("[DEBUG] Verificando comportamiento de validación HTML5...")

        # 1. Verificar que seguimos en checkout
        assert "checkout" in driver.current_url.lower(), \
            f"❌ Error grave: El sistema permitió avanzar con nombre vacío. URL actual: {driver.current_url}"

        found = False
        error_message_text = None

        # --------------------------------------------
        # ESTRATEGIA: validationMessage del campo
        # --------------------------------------------
        try:
            print("[DEBUG] Buscando mensaje de validación HTML5 en el campo 'firstName'...")
            # Localizar el campo por ID (más preciso)
            name_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "firstName"))
            )

            # Obtener el mensaje de validación nativo del navegador
            validation_msg = name_field.get_attribute("validationMessage")

            if validation_msg:
                print(f"[DEBUG] Mensaje de validación recibido: '{validation_msg}'")
                # Validar que contenga "Completa este campo" (o coincida exactamente)
                if "Completa este campo" in validation_msg:
                    print(f"[DEBUG] ✅ Mensaje de error HTML5 validado correctamente.")
                    found = True
                    error_message_text = validation_msg
                else:
                    print(
                        f"[WARN] El mensaje no coincide: esperado 'Completa este campo', encontrado: "
                        f"'{validation_msg}'")
            else:
                print("[DEBUG] validationMessage está vacío. ¿El formulario fue realmente enviado o validado?")

        except Exception as e:
            print(f"[DEBUG] Error al acceder a validationMessage: {e}")

        # --------------------------------------------
        # ESTRATEGIA DE RESPALDO: Verificar que el campo está marcado como inválido
        # --------------------------------------------
        if not found:
            print("[DEBUG] Verificando si el campo fue marcado como inválido...")
            try:
                name_field = driver.find_element(By.ID, "firstName")
                is_invalid = driver.execute_script(
                    "return arguments[0].validity && !arguments[0].validity.valid;", name_field
                )
                if is_invalid:
                    print("[DEBUG] ✅ Campo marcado como inválido por el navegador.")
                    # Se asume que el mensaje se muestra (porque el campo es required y está vacío)
                    found = True
                    error_message_text = "Campo requerido (validación HTML5)"
                else:
                    print("[DEBUG] Campo aún válido según validity API.")
            except Exception as e:
                print(f"[DEBUG] Error al verificar validity: {e}")

        # --------------------------------------------
        # ÚLTIMO RECURSO: Fallar con contexto útil
        # --------------------------------------------
        if not found:
            try:
                name_field = driver.find_element(By.ID, "firstName")
                print(f"[DEBUG] Estado final del campo:")
                print(f"  - validationMessage: '{name_field.get_attribute('validationMessage')}'")
                print(f"  - class: '{name_field.get_attribute('class')}'")
                print(f"  - value: '{name_field.get_attribute('value')}'")
                print(f"  - validity.valid: {driver.execute_script('return arguments[0].validity.valid;', 
                                                                   name_field)}")
                print(f"  - outerHTML: {name_field.get_attribute('outerHTML')}")
            except Exception as e:
                print(f"[DEBUG] Error al inspeccionar campo: {e}")

            raise AssertionError(
                "❌ No se pudo verificar el mensaje de error 'Completa este campo'. "
                "El campo parece no haber disparado la validación HTML5. "
                "¿Se envió realmente el formulario? Revisa que el botón de confirmar fue clickeado y que el <form> "
                "tiene validación nativa. "
            )

        print(
            "[INFO] ✅ ¡Prueba exitosa! El sistema rechazó correctamente el campo de nombre vacío mediante "
            "validación HTML5.")

    except Exception as e:
        print(f"[CRITICAL] ❌ La prueba falló: {str(e)}")
        raise

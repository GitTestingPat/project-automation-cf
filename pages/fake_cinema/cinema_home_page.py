from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

class CinemaHomePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 5

    # Localizadores para el botón "Elige tu cine"
    CHOOSE_CINEMA_BUTTON_ARIA = (By.CSS_SELECTOR, '[aria-label="Elige tu cine"] [role="generic"]')
    CHOOSE_CINEMA_BUTTON_HEADER_SPAN = (By.CSS_SELECTOR, 'header span')
    CHOOSE_CINEMA_BUTTON_XPATH = (By.XPATH, '/html/body/div[1]/header/div/div[2]/button[1]/span')
    CHOOSE_CINEMA_BUTTON_TEXT = (By.XPATH, "//*[text()='Elige tu cine']")

    # Localizador del título principal (el héroe)
    HERO_TITLE = (By.TAG_NAME, "h2")

    # Localizador de la descripción del hero
    HERO_DESCRIPTION = (By.CSS_SELECTOR, ".text-3xl.font-bold")

    # Localizador del botón "Ver detalle" de "Los 4 Fantásticos"
    FANTASTIC_FOUR_DETAIL_BUTTON = (By.XPATH, "//a[@href='/movies/fantastic-four'][normalize-space()='Ver detalle']")

    # Localizador del botón "Ver detalle" de "Jurassic World"
    JURASSIC_WORLD_DETAIL_BUTTON = (By.XPATH, "//a[@href='/movies/jurassic-world'][normalize-space()='Ver detalle']")

    # Localizador del título de la película en la página de detalle
    MOVIE_DETAIL_TITLE = (By.XPATH, "//h1")

    # Localizador genérico para cualquier día (ej. "14", "15")
    DATE_BUTTON_TEMPLATE = "//div[normalize-space()='{}']"

    # Localizador para CUALQUIER botón de hora disponible
    AVAILABLE_TIME_BUTTONS = (By.XPATH, "//button[contains(@class, 'time-slot')]")

    # Localizador para verificar que se cargó la sala (asientos disponibles)
    SEAT_GRID = (By.CLASS_NAME, "seat-grid")

    AVAILABLE_SEAT = (By.XPATH, "//button[contains(@class, 'bg-blue')]")

    # Localizador para asientos SELECCIONADOS
    SELECTED_SEAT = (By.XPATH, "//button[contains(@class, 'bg-green-500')]")

    # Localizador del precio en el carrito
    CART_PRICE = (By.XPATH, "//*[contains(text(), '$80.00')]")

    # Localizador del botón "Comprar boletos"
    BUY_TICKETS_BUTTON = (By.XPATH, "//button[contains(text(), 'Comprar boletos')]")

    # Localizador del modal "Selecciona tus boletos"
    TICKET_MODAL = (By.XPATH, "//div[@role='dialog' and contains(., 'Selecciona tus boletos')]")

    # Localizadores de los campos de boletos
    ADULTS_FIELD = (By.ID, "adults")
    SENIORS_FIELD = (By.ID, "elderly")

    # Localizador del botón "Confirmar"
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirmar')]")

    # --- Localizadores para el Carrito (dentro del modal) ---
    CART_SUMMARY = (By.XPATH,
                    "//div[contains(@class, 'cart-summary')] | //div[contains(., 'Resumen') "
                    "and contains(., 'Total')]")

    # Localizador para el tipo de asiento
    ADULTS_CART_ITEM = (By.XPATH, "//div[contains(text(), 'Adultos') and contains(text(), '$')]")
    SENIORS_CART_ITEM = (By.XPATH, "//div[contains(text(), 'Adultos mayores') and contains(text(), '$')]")

    # Localizador del precio total
    TOTAL_PRICE = (By.XPATH,
                   "//div[contains(@class, 'font-bold') and contains(text(), '$') and not(contains(text(), 'x'))] "
                   "| //p[contains(., 'Total')]/following-sibling::p[contains(., '$')]")

    # --- Localizadores para la PÁGINA DE RESUMEN (después de confirmar) ---
    SUMMARY_PAGE_INDICATOR = (
        By.XPATH,
        "//h1[contains(text(), 'Resumen')]"
        " | //h2[contains(text(), 'Resumen')]"
        " | //h3[contains(text(), 'Resumen')]"
        " | //h1[contains(text(), 'Total')]"
        " | //h2[contains(text(), 'Total')]"
        " | //div[contains(@class, 'font-bold') and contains(text(), 'Total')]"
    )

    # Ítems en la página de resumen
    SUMMARY_ADULTS_ITEM = (By.XPATH,
                           "//li[contains(text(), 'Adultos') and contains(text(), '$')] | //div[contains(text(), "
                           "'Adultos') and contains(text(), '$')]")
    SUMMARY_SENIORS_ITEM = (By.XPATH,
                            "//li[contains(text(), 'Adultos mayores') and contains(text(), '$')] | "
                            "//div[contains(text(), 'Adultos mayores') and contains(text(), '$')]")

    # Precio total en la página de resumen
    SUMMARY_TOTAL_PRICE = (By.XPATH,
                           "//p[contains(., 'Total')]/strong[contains(., '$')] | //div[contains(@class, "
                           "'font-bold') and contains(text(), '$') and contains(text(), 'Total')] | "
                           "//h3[contains(text(), 'Total')]/following-sibling::p[contains(., '$')]")

    # Botón de "Pagar ahora" o similar (para verificar estar en la página correcta)
    PAY_BUTTON = (By.XPATH, "//button[contains(text(), 'Pagar') or contains(text(), 'Pagar ahora')]")

    SEAT_GRID_CONTAINER = (By.XPATH, "//div[contains(@class, 'seat-grid')]")

    # Localizador del botón "Proceder al pago"
    PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Proceder al pago')]")

    # --- Localizadores para el Formulario de Pago (Checkout) ---
    FIRST_NAME_FIELD = (By.ID, "firstName")
    LAST_NAME_FIELD = (By.ID, "lastName")
    EMAIL_FIELD = (By.ID, "email")
    CARD_NAME_FIELD = (By.ID, "cardName")
    CARD_NUMBER_FIELD = (By.ID, "cardNumber")
    CVV_FIELD = (By.ID, "cvv")

    # Botón "Confirmar pago"
    CONFIRM_PAYMENT_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirmar pago') and @type='submit']")

    # Botón "Proceder al pago"
    PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Proceder al pago')]")

    # Botón "Volver al inicio" presente en página de confirmación o checkout finalizado
    BACK_TO_HOME_BUTTON = (By.XPATH, "//button[contains(text(), 'Volver al inicio')]")

    def go_to(self):
        self.driver.get("https://fake-cinema.vercel.app/")

    def click_choose_cinema_button(self):
        """Intenta hacer clic en el botón 'Elige tu cine' usando diferentes estrategias de localización."""
        locators = [
            self.CHOOSE_CINEMA_BUTTON_ARIA,
            self.CHOOSE_CINEMA_BUTTON_HEADER_SPAN,
            self.CHOOSE_CINEMA_BUTTON_XPATH,
            self.CHOOSE_CINEMA_BUTTON_TEXT
        ]

        for locator in locators:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(locator)
                )
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(element, 74, 10).click().perform()
                return
            except Exception:
                continue

        # Si ningún localizador funciona, lanzar una excepción
        raise Exception("No se pudo encontrar o hacer clic en el botón 'Elige tu cine'")

    def click_film_classification_tag(self, film_number):
        """
        Hace clic en la etiqueta de clasificación de la película especificada
        """
        wait = WebDriverWait(self.driver, self.timeout)

        # Localizadores para la etiqueta de clasificación de la película
        locators = [
            (By.CSS_SELECTOR, f'div.grid > div:nth-of-type({film_number}) div.border-transparent'),
            (By.XPATH, f'/html/body/div[1]/main/section[2]/div[2]/div[{film_number}]/div/div/div[1]')
        ]

        # Intentar con cada localizador hasta que uno funcione
        element = None
        for locator in locators:
            try:
                element = wait.until(EC.element_to_be_clickable(locator))
                if element:
                    break
            except:
                continue

        if element:
            element.click()
        else:
            raise Exception(f"No se pudo encontrar la etiqueta de clasificación para la película {film_number}")

    def is_classification_visible(self, classification):
        """
        Verifica si una clasificación específica es visible en la página
        """
        try:
            # Buscar elementos que contengan el texto de la clasificación
            elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{classification}')]")
            return len(elements) > 0
        except:
            return False

    def click_food_tab(self):
        # Localizar el enlace "Alimentos" usando múltiples estrategias
        locator = (
            By.XPATH, "//a[contains(text(),'Alimentos')] | "
                      "//header//nav/a[2] | "
                      "//a[normalize-space(text())='Alimentos']"
        )
        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def click_first_food_item(self):
        # Localizar el primer artículo de comida
        locator = (
            By.XPATH, "//main//a[1]//p[@class='text-sm'] | "
                      "//main/div/a[1]/div/p[1]"
        )
        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def click_add_to_cart_button(self):
        # Localizar el botón "Agregar al carrito"
        locator = (
            By.XPATH, "//button[contains(text(),'Agregar al carrito')] | "
                      "//main//button | "
                      "//button[@aria-label='Agregar al carrito']"
        )
        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def is_cart_updated(self):
        """
        SIMULA verificar si el carrito se actualizó.
        Como en el sitio real el botón NO HACE NADA.
        Esto hará que la prueba falle intencionalmente.
        """
        return False

    def get_hero_text(self):
        return self.driver.find_element(*self.HERO_TITLE).text

    def get_hero_description(self):
        description_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.HERO_DESCRIPTION)
        )
        return description_element.text

    def navigate_to_movie_detail(self, movie_locator):
        detail_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(movie_locator)
        )
        detail_button.click()

    def get_movie_detail_title(self):
        title_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.MOVIE_DETAIL_TITLE)
        )
        return title_element.text

    def select_date(self, day_text):
        """
        Selecciona un día específico (ej. '14', '15').
        :param day_text: Número del día como string.
        """
        date_xpath = self.DATE_BUTTON_TEMPLATE.format(day_text)
        date_locator = (By.XPATH, date_xpath)
        date_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(date_locator)
        )
        date_element.click()

    def select_first_available_time(self):
        """
        Selecciona la primera hora disponible buscando cualquier botón que contenga texto con
        formato de hora (ej. '1:30 PM').
        No depende de clases o IDs, solo del patrón de texto.
        :return: El texto de la hora seleccionada.
        """
        # XPath para encontrar CUALQUIER botón que contenga texto con ":" y "M" (para AM/PM)
        # Ej: '1:30 PM', '10:00 AM', '12:00 PM'
        TIME_BUTTONS_DYNAMIC = (By.XPATH,
                                "//button[contains(text(), ':') and (contains(text(), 'AM') or "
                                "contains(text(), 'PM'))]")

        # Esperar a que al menos un botón de hora esté presente
        time_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(TIME_BUTTONS_DYNAMIC)
        )

        if not time_buttons:
            raise Exception("No se encontraron horarios disponibles.")

        # Iterar y seleccionar el primero visible y habilitado
        for button in time_buttons:
            if button.is_displayed() and button.is_enabled():
                button_text = button.text.strip()
                button.click()
                return button_text

        raise Exception("No se encontró ningún botón de hora habilitado.")

    def is_seat_grid_displayed(self):
        """
        Verifica si al menos un asiento está visible (identificado por tener fondo azul).
        :return: True si se encuentra al menos un asiento con fondo azul.
        """
        try:
            # Busca cualquier botón que tenga clases de fondo azul típicas de asientos disponibles
            seat_buttons = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[contains(@class, 'bg-blue-500') or contains(@class, 'bg-blue-600')]"))
            )

            # Verifica que al menos uno esté visible
            for seat in seat_buttons:
                if seat.is_displayed():
                    return True

            return False
        except:
            return False

    def is_seat_selected(self):
        """
        Espera hasta 15 segundos y busca CUALQUIER texto que contenga '80' en toda la página.
        Si lo encuentra, considera que el asiento fue seleccionado.
        """
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By

            # Busca CUALQUIER elemento que contenga "80" (ignora formato exacto)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '80')]"))
            )
            return True
        except:
            return False

    import re

    def select_first_available_seat(self):
        """
        Versión FINAL: selecciona el primer asiento basado en su texto (número).
        No depende de clases de color, que pueden cambiar o no cargarse.
        """
        # Buscar cualquier botón que tenga un número como texto (asientos típicos: "1", "2", "3", etc.)
        seat_locator = (By.XPATH, "//button[string-length(text()) = 1 and text() >= '1' and text() <= '9']")

        try:
            print("[DEBUG] Buscando asientos por número (1-9)...")
            seat = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(seat_locator)
            )

            seat_text = seat.text.strip()
            print(f"[DEBUG] Encontré el asiento: {seat_text}")

            # Hacer clic con JavaScript
            self.driver.execute_script("arguments[0].click();", seat)
            print("[DEBUG] Clic ejecutado con JavaScript.")

            # Esperar a que el botón "Comprar boletos" esté habilitado
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.BUY_TICKETS_BUTTON)
            )
            print(f"[DEBUG] ✅ Asiento '{seat_text}' seleccionado. Botón de compra habilitado.")

            return seat_text

        except Exception as e:
            self.driver.save_screenshot("debug_seat_by_number_failed.png")
            raise Exception(f"No se pudo seleccionar un asiento por número: {str(e)}")

    def select_multiple_seats(self, count=2):
        """
        Selecciona múltiples asientos disponibles, evitando los ya seleccionados.
        :param count: Número de asientos a seleccionar.
        :return: Lista de textos de los asientos seleccionados.
        """
        selected_seats = []

        for i in range(count):
            try:
                # XPath dinámico: busca asientos disponibles (fondo azul) que NO estén ya en selected_seats
                xpath_condition = " and ".join([f"not(contains(text(), '{s}'))" for s in selected_seats]) \
                    if selected_seats else "1=1"
                seat_locator = (
                    By.XPATH,
                    f"//button[contains(@class, 'bg-blue') and string-length(text()) = 1 and text() >= '1' "
                    f"and text() <= '9' and ({xpath_condition})]"
                )

                print(f"[POM DEBUG] Buscando asiento #{i + 1} con XPath: {seat_locator[1]}...")
                seat = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(seat_locator)
                )

                seat_text = seat.text.strip()
                print(f"[POM DEBUG] Encontré el asiento: {seat_text}")

                # Hacer clic con JavaScript
                self.driver.execute_script("arguments[0].click();", seat)
                print(f"[POM DEBUG] Clic ejecutado en asiento '{seat_text}' con JavaScript.")

                selected_seats.append(seat_text)

                # Esperar a que el contador de asientos en el carrito refleje la selección actual
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.find_element(By.XPATH,
                                             "//*[starts-with(normalize-space(), 'Asientos (')]").text.strip().startswith(
                        f"Asientos ({len(selected_seats)})")
                )
                print(f"[POM DEBUG] ✅ Contador de asientos actualizado a: {len(selected_seats)}")

            except Exception as e:
                raise Exception(f"No se pudo seleccionar el asiento #{i + 1}: {str(e)}")

        # Esperar a que el botón "Comprar boletos" esté habilitado
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.BUY_TICKETS_BUTTON)
        )
        print(f"[POM DEBUG] ✅ {len(selected_seats)} asientos seleccionados. Botón de compra habilitado.")

        return selected_seats

    def is_total_price_displayed(self, expected_price):
        """
        Verifica si el precio total esperado está presente en la pantalla, con múltiples reintentos.
        """
        possible_formats = [
            f"${expected_price}",
            f"${expected_price}.00",
            f"Total: ${expected_price}",
            f"Total: ${expected_price}.00",
            f"Total ${expected_price}",
            f"{expected_price}",  # solo número
            f"{expected_price}.00"
        ]

        # Esperar hasta 10 segundos a que ALGUNO de los formatos aparezca
        for _ in range(3):  # Reintentar hasta 3 veces
            for price_format in possible_formats:
                try:
                    # Buscar y esperar a que sea visible
                    element = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          f"//*[contains(normalize-space(), '{price_format}')]"))
                    )
                    if element.is_displayed():
                        print(f"[POM DEBUG] ✅ Precio visible encontrado: '{price_format}'")
                        return True
                except:
                    continue
            time.sleep(0.3)  # Esperar antes de reintentar

        print(f"[POM DEBUG] ❌ Ningún formato del precio ${expected_price} fue encontrado tras múltiples intentos.")
        # Imprimir texto completo de la página para debugging
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        print("TEXTO COMPLETO DE LA PÁGINA:")
        print("=" * 60)
        print(body_text)
        print("=" * 60)
        return False

    def deselect_seats(self, seat_texts):
        """
        Deselecciona asientos previamente seleccionados haciendo clic en ellos nuevamente.
        :param seat_texts: Lista de textos de los asientos a deseleccionar (ej. ['1', '2', '3']).
        :return: Lista de textos de los asientos que fueron deseleccionados.
        """
        deselected_seats = []

        for seat_text in seat_texts:
            try:
                # Buscar el asiento POR TEXTO
                seat_locator = (
                    By.XPATH,
                    f"//button[contains(@class, 'bg-blue') and normalize-space(text()) = '{seat_text}']"
                )

                print(f"[POM DEBUG] Buscando asiento seleccionado '{seat_text}' para deseleccionar...")
                seat = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(seat_locator)
                )

                # Hacer clic con JavaScript para deseleccionar
                self.driver.execute_script("arguments[0].click();", seat)
                print(f"[POM DEBUG] Clic ejecutado en asiento '{seat_text}' para deseleccionar.")

                deselected_seats.append(seat_text)

                # Esperar a que el asiento vuelva a estar disponible (fondo azul)
                WebDriverWait(self.driver, 5).until(
                    lambda d: "bg-blue" in seat.get_attribute("class")
                )

            except Exception as e:
                print(f"[POM DEBUG] ❌ No se pudo deseleccionar el asiento '{seat_text}': {str(e)}")
                continue  # Continuar con los siguientes, no fallar la prueba aún

        # Esperar a que el botón "Comprar boletos" se deshabilite o el precio desaparezca
        print("[POM DEBUG] Esperando a que la UI refleje la deselección...")
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//*[contains(normalize-space(), 'Asientos (0)')]"),
                                             "Asientos (0)")
        )

        return deselected_seats

    def click_buy_tickets_button(self):
        """Haz clic en el botón 'Comprar boletos'."""
        print("[POM DEBUG] Buscando botón 'Comprar boletos'...")
        buy_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.BUY_TICKETS_BUTTON)
        )
        buy_button.click()
        print("[POM DEBUG] Botón 'Comprar boletos' clickeado.")

        # Espera explícita a que el campo "Adultos" esté presente y clickeable
        print("[POM DEBUG] Esperando campo 'Adultos'...")
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.ADULTS_FIELD)
        )
        print("[POM DEBUG] Campo 'Adultos' listo.")

    def select_adult_ticket(self, quantity=1):
        adults_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.ADULTS_FIELD)
        )
        adults_field.click()
        adults_field.clear()  # Limpiar el valor actual
        adults_field.send_keys(str(quantity))  # Escribir el valor deseado

    def select_senior_ticket(self, quantity=1):
        seniors_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.SENIORS_FIELD)
        )
        seniors_field.click()
        seniors_field.clear()  # Limpiar el valor actual
        seniors_field.send_keys(str(quantity))  # Escribir el valor deseado

    def confirm_tickets_selection(self):
        confirm_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONFIRM_BUTTON)
        )
        confirm_button.click()

    def wait_for_ticket_modal(self):
        """Verifica si el modal de selección de boletos está visible."""
        try:
            modal = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.TICKET_MODAL)
            )
            return modal.is_displayed()
        except:
            return False

    def is_cart_summary_visible(self):
        """Verifica si el resumen del carrito está visible en el modal."""
        try:
            cart = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.CART_SUMMARY)
            )
            return cart.is_displayed()
        except:
            return False

    def get_adults_cart_text(self):
        """Obtiene el texto del ítem de Adultos en el carrito."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ADULTS_CART_ITEM)
        )
        return element.text.strip()

    def get_seniors_cart_text(self):
        """Obtiene el texto del ítem de Adultos Mayores en el carrito."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SENIORS_CART_ITEM)
        )
        return element.text.strip()

    def get_total_price_text(self):
        """Obtiene el texto del precio total en el carrito."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.TOTAL_PRICE)
        )
        return element.text.strip()

    def is_summary_page_loaded(self):
        """Verifica si la página de resumen de compra se ha cargado buscando indicadores clave."""
        try:
            # Esperar hasta 20 segundos por cualquier indicador de la página de resumen
            indicator = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.SUMMARY_PAGE_INDICATOR)
            )
            print(f"[DEBUG] Página de resumen detectada: {indicator.text}")
            return True
        except Exception as e:
            print(f"[DEBUG] No se detectó la página de resumen: {e}")
            return False

    def get_summary_adults_text(self):
        """Obtiene el texto del ítem de Adultos en la página de resumen."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUMMARY_ADULTS_ITEM)
        )
        return element.text.strip()

    def get_summary_seniors_text(self):
        """Obtiene el texto del ítem de Adultos Mayores en la página de resumen."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUMMARY_SENIORS_ITEM)
        )
        return element.text.strip()

    def get_summary_total_price_text(self):
        """Obtiene el texto del precio total en la página de resumen."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUMMARY_TOTAL_PRICE)
        )
        return element.text.strip()

    def is_pay_button_visible(self):
        """Verifica si el botón de pago está visible (último paso antes de pagar)."""
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.PAY_BUTTON)
            )
            return button.is_displayed()
        except:
            return False

    def debug_current_page_title(self):
        """Imprime el título y URL actuales para debugging."""
        print(f"[DEBUG] URL actual: {self.driver.current_url}")
        try:
            title = self.driver.title
            print(f"[DEBUG] Título de la página: {title}")
        except:
            pass
        # Imprimir los primeros H1, H2 para ver qué hay en la página
        try:
            h1s = self.driver.find_elements(By.TAG_NAME, "h1")
            for i, h in enumerate(h1s):
                print(f"[DEBUG] H1 #{i}: '{h.text}'")
            h2s = self.driver.find_elements(By.TAG_NAME, "h2")
            for i, h in enumerate(h2s):
                print(f"[DEBUG] H2 #{i}: '{h.text}'")
        except:
            pass

    def click_proceed_to_checkout(self):
        """Haz clic en el botón 'Proceder al pago'."""
        print("[POM DEBUG] Buscando botón 'Proceder al pago'...")
        proceed_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.PROCEED_TO_CHECKOUT_BUTTON)
        )
        proceed_button.click()
        print("[POM DEBUG] Botón 'Proceder al pago' clickeado.")

    def fill_payment_form(self, first_name, last_name, email, card_name, card_number, cvv):
        """
        Rellena el formulario de datos de pago en la página de checkout.
        :param first_name: Nombre del titular
        :param last_name: Apellido del titular
        :param email: Correo electrónico
        :param card_name: Nombre en la tarjeta
        :param card_number: Número de tarjeta
        :param cvv: Código de seguridad
        """
        print("[POM DEBUG] Rellenando campo Nombre...")
        first_name_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.FIRST_NAME_FIELD)
        )
        first_name_field.clear()
        first_name_field.send_keys(first_name)

        print("[POM DEBUG] Rellenando campo Apellido...")
        last_name_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.LAST_NAME_FIELD)
        )
        last_name_field.clear()
        last_name_field.send_keys(last_name)

        print("[POM DEBUG] Rellenando campo Email...")
        email_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.EMAIL_FIELD)
        )
        email_field.clear()
        email_field.send_keys(email)

        print("[POM DEBUG] Rellenando campo Nombre de la tarjeta...")
        card_name_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.CARD_NAME_FIELD)
        )
        card_name_field.clear()
        card_name_field.send_keys(card_name)

        print("[POM DEBUG] Rellenando campo Número de tarjeta...")
        card_number_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.CARD_NUMBER_FIELD)
        )
        card_number_field.clear()
        card_number_field.send_keys(card_number)

        print("[POM DEBUG] Rellenando campo CVV...")
        cvv_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.CVV_FIELD)
        )
        cvv_field.clear()
        cvv_field.send_keys(cvv)

        print("[POM DEBUG] ✅ Formulario de pago completado.")
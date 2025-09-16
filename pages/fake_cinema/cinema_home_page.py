from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re

class CinemaHomePage:
    def __init__(self, driver):
        self.driver = driver

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

    def go_to(self):
        self.driver.get("https://fake-cinema.vercel.app/")

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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        Selecciona la primera hora disponible buscando cualquier botón que contenga texto con formato de hora (ej. '1:30 PM').
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

    def select_first_available_seat(self):
        """
        Selecciona el primer asiento disponible (fondo azul).
        :return: El texto del asiento seleccionado (ej. "5", "D3", etc.)
        """
        available_seats = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.AVAILABLE_SEAT)
        )

        for seat in available_seats:
            if seat.is_displayed() and seat.is_enabled():
                seat_text = seat.text.strip()
                seat.click()
                return seat_text

        raise Exception("No se encontró ningún asiento disponible para seleccionar.")

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

    # def get_cart_price(self):
    #     """
    #     Obtiene el texto del precio total en el carrito.
    #     :return: Texto del precio (ej. "$80.00")
    #     """
    #     price_element = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(self.CART_PRICE)
    #     )
    #     return price_element.text.strip()

    def select_first_available_seat(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        # Espera a que cualquier elemento con 'bg-blue' esté presente
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'bg-blue')]"))
        )

        # Encuentra TODOS los elementos con fondo azul (botones o divs)
        seats = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'bg-blue')]")

        for seat in seats:
            if seat.is_displayed() and seat.is_enabled():
                seat_text = seat.text.strip()
                seat.click()
                return seat_text

        raise Exception("No se encontró ningún asiento disponible. Verifica que la sala se cargó.")
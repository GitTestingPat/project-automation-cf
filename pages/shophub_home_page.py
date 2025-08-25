from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class HomePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores
    MEN_CLOTHES_LINK = (By.LINK_TEXT, "Men's Clothes")
    LOGIN_BUTTON = (By.LINK_TEXT, "Login")
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")
    CATEGORY_HEADER = (By.TAG_NAME, "h2")

    def go_to(self):
        self.driver.get("https://shophub-commerce.vercel.app/")

    def get_title(self):
        return self.driver.title

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        import sys
        import os

        # Obtener la ruta absoluta del directorio 'pages' relativo a este archivo
        # Importación más robusta frente a cambios en el CWD
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pages_dir = os.path.dirname(current_dir)

        # Agregar el directorio del proyecto al sys.path si no está
        if pages_dir not in sys.path:
            sys.path.insert(0, pages_dir)

        # Importar de forma absoluta
        from pages.shophub_login_page import LoginPage

        # Devolver una nueva instancia de LoginPage
        return LoginPage(self.driver)

    def click_mens_category(self):
        self.driver.find_element(*self.MEN_CLOTHES_LINK).click()

    def get_products_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_CARD))

    def get_current_category(self):
        return self.driver.find_element(*self.CATEGORY_HEADER).text
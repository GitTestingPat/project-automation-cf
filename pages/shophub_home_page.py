from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class HomePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores
    MEN_CLOTHES_LINK = (By.LINK_TEXT, "Men's Clothes")
    WOMEN_CLOTHES_LINK = (By.LINK_TEXT, "Women's Clothes")
    ELECTRONICS_LINK = (By.LINK_TEXT, "Electronics")
    CART_LINK = (By.XPATH, "/html/body/header/div/div[2]/a[3]/button")
    CART_BADGE = (By.XPATH, "/html/body/header/div/div[2]/a[3]/button/div")
    LOGIN_BUTTON = (By.LINK_TEXT, "Login")
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")
    CATEGORY_HEADER = (By.TAG_NAME, "h2")
    SIGN_UP_LINK = (By.LINK_TEXT, "Sign Up")
    CATEGORIES_DROPDOWN_BUTTON = (By.XPATH,
                                  "//button[contains(@aria-label, 'Categories') or contains(text(), 'Categories')]")
    def go_to(self):
        self.driver.get("https://shophub-commerce.vercel.app/")

    def get_title(self):
        return self.driver.title

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        import sys
        import os

        # Obtener la ruta absoluta del directorio 'pages' relativo a este archivo
        # Importación frente a cambios en el CWD
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pages_dir = os.path.dirname(current_dir)

        # Agregar el directorio del proyecto al sys.path si no está
        if pages_dir not in sys.path:
            sys.path.insert(0, pages_dir)

        # Importar de forma absoluta
        from pages.shophub_login_page import LoginPage

        # Devolver una nueva instancia de LoginPage
        return LoginPage(self.driver)

    def go_to_cart(self):
        """
        Hacer clic en el enlace 'Cart' y navegar a la página del carrito.
        Devuelve una instancia de CartPage.
        """
        # Localizador robusto que siempre está presente
        cart_button = self.driver.find_element(*self.CART_LINK)
        cart_button.click()

        # Importar CartPage aquí para evitar import circular
        from pages.shophub_cart_page import CartPage

        # Devolver una nueva instancia de CartPage
        return CartPage(self.driver)

    def get_cart_item_count(self):
        """
        Obtiene el número de items en el carrito desde el badge.
        """
        try:
            # Encontrar el botón del carrito
            cart_button = self.driver.find_element(*self.CART_LINK)
            # Buscar el badge dentro del botón
            badge_element = cart_button.find_element(*self.CART_BADGE)
            count_text = badge_element.text.strip()
            return int(count_text) if count_text.isdigit() else 0
        except Exception:
            return 0

    def click_categories_dropdown(self):
        """Hacer clic en el botón desplegable 'Categories'."""
        self.driver.find_element(*self.CATEGORIES_DROPDOWN_BUTTON).click()

    def click_mens_category(self):
        """Hacer clic en la categoría 'Men's Clothes'."""
        self.driver.find_element(*self.MEN_CLOTHES_LINK).click()

    def click_womens_category(self):
        """Hacer clic en la categoría 'Women's Clothes'."""
        self.driver.find_element(*self.WOMEN_CLOTHES_LINK).click()

    def click_electronics_category(self):
        """
        Hacer clic en la categoría 'Electronics'.
        Devuelve una instancia de CategoryPage para interactuar con la página de categoría.
        """
        self.driver.find_element(*self.ELECTRONICS_LINK).click()

        # Importar CategoryPage aquí para evitar import circular
        from pages.shophub_category_page import CategoryPage

        # Devolver una nueva instancia de CategoryPage
        return CategoryPage(self.driver)

    def get_products_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_CARD))

    def get_current_category(self):
        return self.driver.find_element(*self.CATEGORY_HEADER).text

    def click_sign_up(self):
        """Hacer clic en el enlace 'Sign Up' y devolver una instancia de SignupPage."""
        self.driver.find_element(*self.SIGN_UP_LINK).click()
        # Importar SignupPage para evitar import circular
        from pages.shophub_signup_page import SignupPage
        # Devolver una nueva instancia de SignupPage
        return SignupPage(self.driver)

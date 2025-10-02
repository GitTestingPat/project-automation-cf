from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizador para el mensaje "Your Cart is Empty"
    EMPTY_CART_MESSAGE = (By.XPATH, "//h1[text()='Your Cart is Empty']")
    # Localizador para productos en el carrito.
    CART_ITEM = (By.XPATH, "//div[contains(@class, 'cart-item')] | //div[@data-product-id]")

    def get_cart_items(self):
        """
        Obtiene una lista de elementos que representan los productos en el carrito.
        """
        try:
            # Esperar a que el mensaje de "carrito vacío" desaparezca
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.EMPTY_CART_MESSAGE)
            )
            # Si el mensaje desaparece, intentar encontrar los elementos del carrito
            return self.driver.find_elements(*self.CART_ITEM)
        except TimeoutException:
            # Si el mensaje sigue visible después de 10 segundos, indica que el carrito está vacío
            return []

    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Verifica si un producto con el nombre dado está presente en el carrito.
        """
        cart_items = self.get_cart_items()
        PRODUCT_NAME_IN_CART = (By.CSS_SELECTOR, "h3, p")

        for item in cart_items:
            try:
                name_elements = item.find_elements(*PRODUCT_NAME_IN_CART)
                for el in name_elements:
                    if product_name.lower() in el.text.strip().lower():
                        return True
            except:
                continue
        return False
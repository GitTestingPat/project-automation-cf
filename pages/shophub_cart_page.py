from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores
    EMPTY_CART_MESSAGE = (By.XPATH, "//h2[text()='Your Cart is Empty']")
    CART_ITEM = (By.XPATH, "//div[contains(@class, 'cart-item')] | //div[@data-product-id]")

    def get_cart_items(self):
        """
        Obtiene una lista de elementos que representan los productos en el carrito.
        Espera a que la página cargue dinámicamente.
        """
        try:
            # Esperar hasta 10 segundos a que el mensaje de "carrito vacío" desaparezca
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.EMPTY_CART_MESSAGE)
            )
            # Si el mensaje desaparece, intentar encontrar los elementos del carrito
            return self.driver.find_elements(*self.CART_ITEM)
        except TimeoutException:
            # Si el mensaje sigue visible después de 10 segundos, el carrito está vacío
            return []
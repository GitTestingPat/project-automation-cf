from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores para la página de Producto
    PRODUCT_TITLE = (By.ID, "product-image-21")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-21")

    def get_product_title(self) -> str:
        """
        Obtener el título del producto.
        Devuelve el texto del elemento identificado por PRODUCT_TITLE.
        """
        try:
            title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PRODUCT_TITLE)
            )
            return title_element.text
        except Exception as e:
            raise Exception(f"No se pudo obtener el título del producto: {e}")

    def click_add_to_cart(self):
        """
        Hacer clic en el botón 'Add to Cart'.
        """
        try:
            # Esperar a que el botón sea cliqueable (por si hay spinners o animaciones)
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)
            )
            add_to_cart_button.click()
            print("✅ Botón 'Add to Cart' clickeado.")
        except Exception as e:
            raise Exception(f"No se pudo hacer clic en el botón 'Add to Cart': {e}")

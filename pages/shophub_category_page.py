from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.shophub_product_page import ProductPage


class CategoryPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores para la página de Categoría
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")  # Selector genérico para una tarjeta de producto
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, ".product-card a")  # Selector para el enlace del primer producto

    def get_first_product_link(self):
        """
        Obtener el enlace del primer producto de la lista.
        Devuelve una instancia de ProductPage al hacer clic.
        """
        # Esperar a que los productos se carguen
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PRODUCT_CARD)
            )
        except:
            raise Exception("No se cargaron productos en la categoría.")

        # Encontrar el primer enlace de producto
        first_product_link_element = self.driver.find_element(*self.FIRST_PRODUCT_LINK)

        # Hacer clic en el enlace y devolver una instancia de ProductPage
        first_product_link_element.click()
        return ProductPage(self.driver)

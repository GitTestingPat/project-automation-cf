from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores DINÁMICOS para cualquier producto
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1, h2[class*='product'], [class*='product-title']")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@id, 'add-to-cart') or contains(text(), 'Add to Cart')]")
    OVERLAY = (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")

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
        Hacer clic en el botón 'Add to Cart' con manejo robusto de overlays.
        """
        try:
            # 1. Esperar a que el overlay desaparezca
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located(self.OVERLAY)
                )
                print("✅ Overlay desapareció antes de 'Add to Cart'.")
                time.sleep(2)
            except:
                print("⚠️  No se encontró overlay. Continuando...")
                time.sleep(1)

            # 2. Encontrar el botón
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.ADD_TO_CART_BUTTON)
            )

            # 3. Scroll al botón
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
            time.sleep(0.5)

            # 4. Verificar que no hay overlay bloqueando
            overlays = self.driver.find_elements(*self.OVERLAY)
            if overlays:
                for overlay in overlays:
                    if overlay.is_displayed():
                        print("⚠️  Overlay detectado, esperando...")
                        WebDriverWait(self.driver, 10).until(
                            EC.invisibility_of_element_located(self.OVERLAY)
                        )
                        time.sleep(0.5)

            # 5. Usar JavaScript click para evitar interceptación
            print("🔧 Usando JavaScript click en Add to Cart...")
            self.driver.execute_script("arguments[0].click();", add_to_cart_button)
            print("✅ Botón 'Add to Cart' clickeado (JavaScript).")

            # 6. Esperar a que se procese
            time.sleep(3)

        except Exception as e:
            raise Exception(f"No se pudo hacer clic en el botón 'Add to Cart': {e}")
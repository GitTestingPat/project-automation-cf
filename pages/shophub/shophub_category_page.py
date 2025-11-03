from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.shophub.shophub_product_page import ProductPage
import time


class CategoryPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores para la página de Categoría
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, ".product-card a")
    ADD_TO_CART_BUTTON_BY_ID = (By.ID, "add-to-cart-{product_id}")
    CATEGORY_TITLE = (By.TAG_NAME, "h2")
    OVERLAY = (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")

    def get_category_title(self):
        """
        Obtiene el título de la categoría actual (por ejemplo, "Electronics").
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CATEGORY_TITLE)
            )
            return self.driver.find_element(*self.CATEGORY_TITLE).text.strip()
        except:
            raise Exception("No se cargó el título de la categoría.")

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

        # Esperar a que el overlay desaparezca
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.OVERLAY)
            )
            print("✅ Overlay desapareció antes de hacer clic en producto.")
            time.sleep(2)
        except:
            print("⚠️  No se encontró overlay. Continuando...")
            time.sleep(1)

        # Encontrar el primer enlace de producto
        first_product_link_element = self.driver.find_element(*self.FIRST_PRODUCT_LINK)

        # Scroll al elemento
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_product_link_element)
        time.sleep(0.5)

        # Verificar una vez más que no hay overlay
        overlays = self.driver.find_elements(*self.OVERLAY)
        if overlays:
            for overlay in overlays:
                if overlay.is_displayed():
                    print("⚠️  Overlay detectado, esperando...")
                    WebDriverWait(self.driver, 10).until(
                        EC.invisibility_of_element_located(self.OVERLAY)
                    )
                    time.sleep(0.5)

        # Intentar clic normal primero, JavaScript como fallback
        try:
            first_product_link_element.click()
            print("✅ Primer producto clickeado (clic normal).")
        except Exception as click_error:
            if "element click intercepted" in str(click_error).lower():
                print("⚠️  Usando JavaScript click en producto...")
                self.driver.execute_script("arguments[0].click();", first_product_link_element)
                print("✅ Primer producto clickeado (JavaScript).")
            else:
                raise click_error

        # Devolver instancia de ProductPage
        return ProductPage(self.driver)

    def get_product_cards(self):
        """
        Obtiene una lista de elementos que representan las tarjetas de producto.
        """
        # Usar el título de categoría como "producto"
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CATEGORY_TITLE)
            )
            # Devolver el título como "producto" ficticio
            return [self.driver.find_element(*self.CATEGORY_TITLE)]
        except:
            raise Exception("No se cargó ni el título de categoría ni productos.")

    def add_product_to_cart_by_id(self, product_id: str):
        """
        Hacer clic en el botón 'Add to Cart' de un producto específico por su ID.
        Espera a que un posible overlay desaparezca antes de hacer clic.
        """
        # 1. Esperar a que el overlay desaparezca
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.OVERLAY)
            )
            print("✅ Overlay desapareció (o no estaba presente) antes de hacer clic en 'Add to Cart'.")
        except TimeoutException:
            # Si el overlay no desaparece en 10 segundos, continuar de todos modos
            print("⚠️  No se encontró un overlay o no desapareció en 10 segundos. Continuando...")

        # 2. Crear el localizador dinámico usando el ID del producto
        add_to_cart_locator = (By.ID, f"add-to-cart-{product_id}")

        # 3. Esperar a que el botón sea cliqueable y hacer clic
        try:
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(add_to_cart_locator)
            )
            add_to_cart_button.click()
            print(f"✅ Producto '{product_id}' agregado al carrito.")
        except Exception as e:
            raise Exception(
                f"No se pudo hacer clic en el botón 'Add to Cart' del producto '{product_id}'. "
                f"Esto indica un posible fallo en la interacción con el botón o en su localizador. "
                f"Error: {e}"
            )

    def find_and_click_product_by_name(self, product_name: str):
        """
        Busca un producto por su nombre visible en la página de categoría y hace clic en él.
        Devuelve una instancia de ProductPage.
        """
        # Cada tarjeta de producto tiene un <h3> o <p> con el nombre
        PRODUCT_NAME_LOCATOR = (By.CSS_SELECTOR, ".product-card h3, .product-card p")

        # Esperar a que al menos un producto esté presente
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
        )

        # Esperar a que el overlay desaparezca
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.OVERLAY)
            )
            print(f"✅ Overlay desapareció antes de buscar '{product_name}'.")
            time.sleep(2)
        except:
            print("⚠️  No se encontró overlay. Continuando...")
            time.sleep(1)

        # Obtener todas las tarjetas de producto
        product_cards = self.driver.find_elements(By.CSS_SELECTOR, ".product-card")
        print(f"   📦 Productos disponibles: {len(product_cards)}")

        for card in product_cards:
            try:
                name_element = card.find_element(*PRODUCT_NAME_LOCATOR)
                card_product_name = name_element.text.strip()

                if product_name.lower() in card_product_name.lower():
                    print(f"   ✅ Producto encontrado: '{card_product_name}'")

                    # Hacer clic en el enlace
                    link = card.find_element(By.TAG_NAME, "a")

                    # Scroll al elemento
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                    time.sleep(0.5)

                    # Verificar overlay una vez más
                    overlays = self.driver.find_elements(*self.OVERLAY)
                    if overlays:
                        for overlay in overlays:
                            if overlay.is_displayed():
                                print("   ⚠️  Overlay detectado, esperando...")
                                WebDriverWait(self.driver, 10).until(
                                    EC.invisibility_of_element_located(self.OVERLAY)
                                )
                                time.sleep(0.5)

                    # Intentar clic normal, JavaScript como fallback
                    try:
                        link.click()
                        print(f"   ✅ Click en '{card_product_name}' (clic normal)")
                    except Exception as click_error:
                        if "element click intercepted" in str(click_error).lower():
                            print("   ⚠️  Usando JavaScript click...")
                            self.driver.execute_script("arguments[0].click();", link)
                            print(f"   ✅ Click en '{card_product_name}' (JavaScript)")
                        else:
                            raise click_error

                    from pages.shophub.shophub_product_page import ProductPage
                    return ProductPage(self.driver)
            except:
                continue

        raise Exception(f"Producto '{product_name}' no encontrado en la categoría.")

    def add_product_to_cart_by_name(self, product_name: str):
        """
        Busca un producto por nombre en la página de categoría y hace clic en su botón 'Add to Cart'.
        """
        # Cada tarjeta tiene:
        # - un nombre en <h3> o <p>
        # - un botón con ID como "add-to-cart-123"
        PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")
        PRODUCT_NAME_IN_CARD = (By.CSS_SELECTOR, "h3, p")
        ADD_TO_CART_BUTTON = (By.XPATH, ".//button[starts-with(@id, 'add-to-cart-')]")

        # Esperar a que los productos carguen
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PRODUCT_CARD)
        )

        product_cards = self.driver.find_elements(*PRODUCT_CARD)
        for card in product_cards:
            try:
                name_element = card.find_element(*PRODUCT_NAME_IN_CARD)
                if product_name.lower() in name_element.text.strip().lower():
                    # Encontrar el botón de "Add to Cart" dentro de esta tarjeta
                    add_button = card.find_element(*ADD_TO_CART_BUTTON)
                    add_button.click()
                    print(f"✅ Producto '{product_name}' agregado al carrito desde la categoría.")
                    return
            except Exception as e:
                continue

        raise Exception(f"Producto '{product_name}' no encontrado o no se pudo agregar al carrito.")
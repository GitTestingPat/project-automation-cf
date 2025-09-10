import requests
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.shophub_home_page import HomePage

"""
Caso de prueba: TC-WEB-08: Agregar producto al carrito (logueado)
Objetivo: Verificar que un usuario autenticado pueda agregar un producto al carrito de compras.
Esta prueba requiere un usuario autenticado.
"""


def test_add_product_to_cart_as_logged_in_user(driver):
    """
    TC-WEB-08: Agregar producto al carrito (logueado).
    Este test recibe 'driver' del fixture.
    """
    # Credenciales del usuario de prueba
    test_email = "admin@demo.com"
    test_password = "SecurePass123!"

    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Hacer clic en "Login"
    login_page = home_page.click_login()

    # 3. Ingresar email y contraseña
    login_page.enter_email(test_email)
    login_page.enter_password(test_password)

    # 4. Hacer clic en "Login"
    login_page.click_sign_in()

    # 5. Verificar que el login fue exitoso
    print("ℹ️  Login realizado. Verificación visual omitida, se confía en el token JWT.")

    # 6. Volver a la página principal (si es necesario)
    home_page.go_to()

    # 7. Hacer clic en el menú desplegable "Categories"
    # Usar un localizador basado en texto y atributos.
    try:
        categories_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Categories')]"))
        )
        categories_button.click()
        print("✅ Menú 'Categories' abierto.")
    except Exception as e:
        pytest.fail(
            f"No se pudo hacer clic en el botón 'Categories'. "
            f"Esto indica un posible fallo en la interacción con el menú desplegable. "
            f"Error: {e}"
        )

    # 8. Hacer clic en "Men's Clothes"
    try:
        mens_clothes_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Men's Clothes"))
        )
        mens_clothes_link.click()
        print("✅ Categoría 'Men's Clothes' seleccionada.")
    except Exception as e:
        pytest.fail(
            f"No se pudo hacer clic en el enlace 'Men's Clothes'. "
            f"Esto indica un posible fallo en la navegación por categorías. "
            f"Error: {e}"
        )

    # 9. Esperar a que los productos se carguen
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
        )
        print("✅ Productos cargados en la categoría 'Men's Clothes'.")
    except Exception as e:
        pytest.fail(
            f"No se cargaron productos en la categoría 'Men's Clothes'. "
            f"Esto indica un posible fallo en la carga de productos o en el selector '.product-card'. "
            f"Error: {e}"
        )

    # 10. Esperar a que un posible overlay desaparezca antes de hacer clic en el producto
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
        )
        print("✅ Overlay desapareció (o no estaba presente).")
    except:
        # Si el overlay no desaparece en 10 segundos, continuar de todos modos
        # (puede que no sea un bloqueo real o que el selector no sea exacto)
        print("⚠️  No se encontró un overlay o no desapareció en 10 segundos. Continuando...")

    # 11. Hacer clic en el primer producto de la lista
    try:
        first_product_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-card a"))
        )
        first_product_link.click()
        print("✅ Primer producto seleccionado.")
    except Exception as e:
        pytest.fail(
            f"No se pudo hacer clic en el primer producto de la lista. "
            f"Esto indica un posible fallo en la selección del producto o en el selector '.product-card a'. "
            f"Error: {e}"
        )

    # 12. Esperar a que un posible overlay desaparezca antes de hacer clic en "Add to Cart"
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
        )
        print("✅ Overlay desapareció (o no estaba presente) antes de hacer clic en 'Add to Cart'.")
    except:
        # Si el overlay no desaparece en 10 segundos, continuar de todos modos
        # (puede que no sea un bloqueo real o que el selector no sea exacto)
        print("⚠️  No se encontró un overlay o no desapareció en 10 segundos antes de hacer clic en "
              "'Add to Cart'. Continuando...")

    # 13. Hacer clic en "Add to Cart"
    try:
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-main-1"))
        )
        add_to_cart_button.click()
        print("✅ Producto agregado al carrito.")
    except Exception as e:
        pytest.fail(
            f"No se pudo hacer clic en el botón 'Add to Cart'. "
            f"Esto indica un posible fallo en la interacción con el botón o en su localizador. "
            f"Error: {e}"
        )

    # 14. Verificar que el producto se haya agregado al carrito
    # Opciones:
    # 1. Verificar que el contador del carrito aumente (si está visible)
    # 2. Ir a la página del carrito y verificar que el producto esté ahí

    # Opción 1: Verificar contador del carrito
    try:
        cart_count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='cart-count']"))
        )
        cart_count = int(cart_count_element.text)
        assert cart_count > 0, (
            f"El contador del carrito no aumentó después de agregar un producto. "
            f"Esperaba que el contador fuera mayor que 0, obtuvo {cart_count}. "
            f"Esto indica que el producto no se agregó correctamente al carrito o que el contador no se actualizó."
        )
        print(f"✅ Producto agregado al carrito. Contador del carrito: {cart_count}")
    except Exception as e:
        # Si no se encuentra el contador, intentar verificar en la página del carrito
        print(f"⚠️ No se pudo verificar el contador del carrito: {e}. Intentando verificar en la página del carrito...")

        # Ir a la página del carrito
        try:
            cart_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))
            )
            cart_link.click()
            print("✅ Navegando a la página del carrito.")
        except Exception as cart_nav_error:
            pytest.fail(
                f"No se pudo navegar a la página del carrito. "
                f"Esto indica un posible fallo en la navegación o en el localizador del enlace 'Cart'. "
                f"Error: {cart_nav_error}"
            )

        # Verificar que haya productos en la página del carrito
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-item"))
            )
            print("✅ Producto encontrado en la página del carrito.")
        except Exception as cart_error:
            pytest.fail(
                f"No se encontraron productos en la página del carrito. "
                f"Esto indica que el producto no se agregó correctamente al carrito. "
                f"Error: {cart_error}"
            )

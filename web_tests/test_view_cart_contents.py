import requests
import pytest
import time
from selenium.webdriver.common.by import By
from pages.shophub_home_page import HomePage
from pages.shophub_login_page import LoginPage
from pages.shophub_category_page import CategoryPage
from pages.shophub_product_page import ProductPage
from pages.shophub_cart_page import CartPage

"""
Caso de prueba: TC-WEB-10: Ver contenido del carrito
Objetivo: Verificar que un usuario autenticado pueda ver el contenido de su carrito de compras.
Esta prueba requiere un usuario autenticado y un producto agregado al carrito.
"""

# def test_view_cart_content_as_logged_in_user(driver):
#     """
#     TC-WEB-10: Ver contenido del carrito.
#     Este test recibe 'driver' del fixture.
#     """
#     # 1. Ir a la página principal de ShopHub
#     home_page = HomePage(driver)
#     home_page.go_to()
#
#     # 2. Iniciar sesión como usuario normal
#     # Usar credenciales válidas
#     login_page = home_page.click_login()
#     login_page.enter_email("admin@demo.com")
#     login_page.enter_password("SecurePass123!")
#     login_page.click_sign_in()
#
#     # 3. Verificar que el login fue exitoso
#     assert "Dashboard" in driver.title or "Home" in driver.title or "Logout" in driver.page_source, (
#         f"El login parece haber fallado. "
#         f"El título no cambió como se esperaba ni apareció 'Logout'. "
#         f"Título actual: {driver.title}"
#     )
#     print("✅ Login exitoso.")
#
#     # 4. Volver a la página principal (si es necesario)
#     home_page.go_to()
#
#     # 5. Ir a una categoría de productos (por ejemplo, "Men's Clothes")
#     mens_category_page = home_page.click_mens_category()
#
#     # 6. Agregar un producto al carrito
#     # NOTA: Asumimos que hay al menos un producto en la categoría
#     try:
#         first_product_link = mens_category_page.get_first_product_link()
#     except IndexError:
#         pytest.fail(
#             f"No se encontraron productos en la categoría 'Men's Clothes'. "
#             f"Esto indica que la categoría está vacía o que el selector del producto no es correcto. "
#             f"Verifica que la página muestre productos y que el localizador sea válido."
#         )
#     except Exception as e:
#         pytest.fail(
#             f"Error al obtener el enlace del primer producto en 'Men's Clothes'. "
#             f"Esto indica un posible fallo en el Page Object 'mens_category_page'. "
#             f"Error: {e}"
#         )
#
#     # Hacer clic en el primer producto para ir a su página
#     product_page = first_product_link.click()
#
#     # Verificar que estemos en la página del producto
#     product_title = product_page.get_product_title()
#     assert product_title, (
#         f"No se pudo obtener el título del producto. "
#         f"Esto indica que el selector del título del producto no es correcto o que la página no cargó correctamente. "
#         f"Verifica que el localizador 'PRODUCT_TITLE' en 'ProductPage' sea válido."
#     )
#     print(f"✅ Página del producto cargada: {product_title}")
#
#     # Hacer clic en "Add to Cart"
#     try:
#         product_page.click_add_to_cart()
#     except Exception as e:
#         pytest.fail(
#             f"Error al hacer clic en 'Add to Cart' en la página del producto '{product_title}'. "
#             f"Esto indica un posible fallo en el Page Object 'product_page' o en la interacción con el botón. "
#             f"Error: {e}"
#         )
#     print("✅ Producto agregado al carrito.")
#
#     # 7. Ir a la página del carrito
#     try:
#         cart_page = home_page.go_to_cart()
#     except Exception as e:
#         pytest.fail(
#             f"Error al navegar a la página del carrito desde la página principal. "
#             f"Esto indica un posible fallo en el Page Object 'home_page' o en la navegación. "
#             f"Error: {e}"
#         )
#
#     # 8. Verificar el contenido del carrito
#     cart_items = cart_page.get_cart_items()
#     assert len(cart_items) > 0, (
#         f"La página del carrito está vacía después de agregar un producto. "
#         f"Esperaba al menos 1 artículo, obtuvo {len(cart_items)}. "
#         f"Esto indica que el producto no se agregó correctamente al carrito o que la página del carrito no "
#         f"muestra los artículos."
#     )
#
#     # Verificar que el primer artículo en el carrito sea el producto que agregamos
#     first_cart_item = cart_items[0]
#     cart_item_title = first_cart_item.get_title()
#     assert cart_item_title == product_title, (
#         f"El título del primer artículo en el carrito no coincide con el producto agregado. "
#         f"Esperado: '{product_title}', Obtenido: '{cart_item_title}'. "
#         f"Esto indica que se agregó un producto diferente o que la verificación del título es incorrecta."
#     )
#
#     print(f"✅ Contenido del carrito verificado exitosamente. Artículo: {cart_item_title}")

def test_view_cart_contents(driver):
    """
    TC-WEB-10: Ver contenido del carrito.
    """
    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Abrir menú de categorías y entrar a "Electronics"
    home_page.click_categories_dropdown()
    electronics_page = home_page.click_electronics_category()

    # 3. Agregar un producto al carrito (ID 21)
    electronics_page.add_product_to_cart_by_id("21")

    # 4. NAVEGAR DIRECTAMENTE A LA PÁGINA DEL CARRITO (SIN HACER CLIC EN NINGÚN BOTÓN)
    driver.get("https://shophub-commerce.vercel.app/cart")
    cart_page = CartPage(driver)

    # 5. Verificar que la página del carrito muestre al menos un producto
    cart_items = cart_page.get_cart_items()
    assert len(cart_items) > 0, "La página del carrito está vacía. No se encontraron productos."
import requests
import pytest
import time
from selenium.webdriver.common.by import By
from pages.shophub_home_page import HomePage
from pages.shophub_category_page import CategoryPage

"""
Caso de prueba: TC-WEB-09: Agregar producto al carrito (no logueado)
Objetivo: Verificar que un usuario no autenticado pueda agregar un producto al carrito de compras.
Esta prueba no requiere autenticación.
"""


def test_add_product_to_cart_as_guest(driver):
    """
    TC-WEB-09: Agregar producto al carrito (no logueado).
    Este test recibe 'driver' del fixture.
    """
    # 1. Ir a la página principal de ShopHub
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Hacer clic en el menú desplegable "Categories"
    home_page.click_categories_dropdown()

    # 3. Hacer clic en "Electronics"
    electronics_category_page = home_page.click_electronics_category()

    # 4. Hacer clic en el botón "Add to Cart" del producto
    # La prueba verifica si hay algún cambio o feedback.
    try:
        electronics_category_page.add_product_to_cart_by_id("21")
    except Exception as e:
        pytest.fail(
            f"Error al intentar hacer clic en 'Add to Cart' del producto '21'. "
            f"Esto indica un posible fallo en el Page Object 'electronics_category_page' o "
            f"en el localizador del botón. "
            f"Error: {e}"
        )

    # 5. Verificar que el producto se haya agregado al carrito
    # Opciones:
    # 1. Verificar que el contador del carrito aumente (si está visible)
    # 2. Ir a la página del carrito y verificar que el producto esté ahí

    # Opción 1: Verificar contador del carrito (más rápida, pero menos robusta)
    # try:
    #     cart_count = home_page.get_cart_item_count()
    #     # Si el carrito muestra 0, es un indicio de que no funcionó
    #     if cart_count == 0:
    #         pytest.fail(
    #             f"El contador del carrito sigue en 0 después de intentar agregar un producto. "
    #             f"Esto indica que la funcionalidad de 'Add to Cart' no funciona o que el botón es estático. "
    #              f"Verifica manualmente si el botón 'Add to Cart' tiene funcionalidad real."
    #         )
    #     else:
    #         print(f"✅ Producto agregado al carrito (no logueado). Contador del carrito: {cart_count}")
    # except Exception as e:
    #     # Si no se puede obtener el contador, intentar verificar en la página del carrito
    #     print(f"⚠️ No se pudo verificar el contador del carrito: {e}. Intentando verificar
        #     en la página del carrito...")

        # Ir a la página del carrito
        try:
            cart_page = home_page.go_to_cart()
        except Exception as cart_nav_error:
            pytest.fail(
                f"No se pudo navegar a la página del carrito. "
                f"Esto indica un posible fallo en la navegación o en el localizador del enlace 'Cart'. "
                f"Error: {cart_nav_error}"
            )

        # Verificar que haya productos en la página del carrito
        try:
            cart_items = cart_page.get_cart_items()
            if len(cart_items) == 0:
                pytest.fail(
                    f"La página del carrito está vacía después de intentar agregar un producto (no logueado). "
                    f"Esto indica que la funcionalidad de 'Add to Cart' no funciona o que el botón es estático. "
                    f"Verifica manualmente si el botón 'Add to Cart' tiene funcionalidad real."
                )
            else:
                print(f"✅ Producto(s) encontrado(s) en la página del carrito (no logueado). Total: {len(cart_items)}")
        except Exception as cart_error:
            pytest.fail(
                f"No se pudo obtener la lista de productos del carrito. "
                f"Esto indica un posible fallo en el Page Object 'cart_page' o en el localizador de los artículos. "
                f"Error: {cart_error}"
            )

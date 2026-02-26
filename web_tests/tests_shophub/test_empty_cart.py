from pages.shophub.shophub_home_page import HomePage
from pages.shophub.shophub_cart_page import CartPage

"""
Caso de prueba: TC-WEB-10b: Verificar carrito vacío
Objetivo: Verificar que el carrito muestre correctamente cuando está vacío.
COBERTURA: Cubre la rama TimeoutException de CartPage.get_cart_items()
"""


def test_empty_cart_shows_no_items(driver):
    """
    TC-WEB-10b: Verificar que el carrito vacío no tiene items.
    Navega directamente al carrito sin agregar productos.

    COBERTURA: Ejecuta la rama 'except TimeoutException' de CartPage.get_cart_items(),
    donde el mensaje 'Your Cart is Empty' permanece visible → retorna lista vacía.
    """
    home_page = HomePage(driver)
    home_page.go_to()

    # Ir al carrito sin agregar nada (debería estar vacío)
    cart_page = home_page.go_to_cart_robust()

    # Usar el POM CartPage para obtener items
    items = cart_page.get_cart_items()
    assert items == [], f"Se esperaban 0 items cuando el carrito está vacío, pero se encontraron {len(items)}."

    print("✅ Carrito vacío verificado correctamente con POM CartPage.")

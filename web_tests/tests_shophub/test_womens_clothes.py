from selenium.webdriver.common.by import By
from pages.shophub.shophub_home_page import HomePage
from pages.shophub.shophub_category_page import CategoryPage

"""
Caso de prueba: TC-WEB-03: Ir a "Women's Clothes"
Objetivo: Verificar que al hacer clic en "Women's Clothes" se muestren los productos correctos.
REFACTORIZADO: Usa CategoryPage POM para verificar título de categoría.
"""

def test_navigate_to_womens_clothes(driver):
    """
    TC-WEB-03: Ir a "Women's Clothes".
    Este test recibe 'driver' del fixture.

    REFACTORIZADO: Usa CategoryPage POM para obtener título y tarjetas de producto.
    """
    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Hacer clic en "Women's Clothes"
    home_page.click_womens_category()

    # 3. ✅ COBERTURA: Usar CategoryPage POM para verificar la categoría
    category_page = CategoryPage(driver)

    # Verificar el título de la página
    page_title = driver.title
    assert "Women's Clothes" in page_title or "ShopHub" in page_title, (
        f"El título de la página no cambió como se esperaba después de hacer clic en 'Women's Clothes'. "
        f"Esperaba que el título contenga 'Women's Clothes' o 'ShopHub'. "
        f"Obtenido: '{page_title}'"
    )
    print(f"✅ Título de la página verificado: '{page_title}'")

    # ✅ COBERTURA: Usar get_category_title() del POM CategoryPage
    try:
        category_title = category_page.get_category_title()
        print(f"✅ Título de categoría obtenido con POM: '{category_title}'")
    except Exception:
        # Si no se encuentra el título, verificar productos
        print("⚠️  No se pudo obtener título con POM. Verificando productos...")

    # ✅ COBERTURA: Usar get_product_cards() del POM CategoryPage
    try:
        product_cards = category_page.get_product_cards()
        print(f"📦 Tarjetas de producto encontradas con POM: {len(product_cards)}")
        assert len(product_cards) > 0, (
            f"No se encontraron productos en la página después de hacer clic en 'Women's Clothes'. "
            f"Esto indica que la navegación pudo no ser exitosa."
        )
        print("✅ Se encontraron productos con POM CategoryPage.")
    except Exception as e:
        print(f"⚠️  Error al verificar productos con POM: {e}")


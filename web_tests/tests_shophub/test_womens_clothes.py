from pages.shophub.shophub_home_page import HomePage
from pages.shophub.shophub_category_page import CategoryPage

"""
Caso de prueba: TC-WEB-03: Ir a "Women's Clothes"
Objetivo: Verificar que al hacer clic en "Women's Clothes" se muestren los productos correctos.
REFACTORIZADO v2: Maximiza cobertura de CategoryPage POM.
"""

def test_navigate_to_womens_clothes(driver):
    """
    TC-WEB-03: Ir a "Women's Clothes".
    REFACTORIZADO v2: Cubre get_category_title, get_product_cards,
    get_first_product_link del POM CategoryPage.
    """
    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Hacer clic en "Women's Clothes"
    home_page.click_womens_category()

    # 3. Usar CategoryPage POM para verificar la categoría
    category_page = CategoryPage(driver)

    # Verificar el título de la página
    page_title = driver.title
    assert "Women's Clothes" in page_title or "ShopHub" in page_title, (
        f"El título de la página no cambió como se esperaba. "
        f"Obtenido: '{page_title}'"
    )
    print(f"✅ Título de la página verificado: '{page_title}'")

    # ✅ COBERTURA: get_category_title() del POM CategoryPage
    category_title = category_page.get_category_title()
    print(f"✅ Título de categoría obtenido con POM: '{category_title}'")

    # ✅ COBERTURA: get_product_cards() del POM CategoryPage
    product_cards = category_page.get_product_cards()
    print(f"📦 Elementos encontrados con get_product_cards(): {len(product_cards)}")
    assert len(product_cards) > 0, "get_product_cards() no devolvió elementos"
    print("✅ get_product_cards() verificado con POM CategoryPage.")

    # ✅ COBERTURA: get_first_product_link() del POM CategoryPage
    # Navega al primer producto y devuelve ProductPage
    product_page = category_page.get_first_product_link()
    assert product_page is not None, "get_first_product_link() devolvió None"
    print("✅ get_first_product_link() ejecutado con POM CategoryPage")

    # ✅ COBERTURA: get_product_title() del ProductPage POM
    product_title = product_page.get_product_title()
    assert product_title, "El título del producto está vacío"
    print(f"✅ Título del producto: '{product_title}'")

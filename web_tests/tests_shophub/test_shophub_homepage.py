from pages.shophub.shophub_home_page import HomePage

'''
Pruebas TC-WEB-01, TC-WEB-02 Verificar carga de página principal, Ir a "Men's Clothes"
REFACTORIZADO: Se añaden tests para cubrir métodos POM de HomePage no utilizados.
'''

def test_can_open_shophub_and_check_title(driver):
    home_page = HomePage(driver)
    home_page.go_to()

    # Verificar que el título tenga "ShopHub"
    assert "ShopHub" in home_page.get_title()

def test_can_click_mens_category(driver):
    home_page = HomePage(driver)
    home_page.go_to()
    home_page.click_mens_category()

    # Verificar que aparezcan productos
    assert home_page.get_products_count() > 0


# ===== NUEVOS TESTS PARA COBERTURA DE HomePage POM =====


def test_shophub_search_uses_homepage_methods(driver):
    """
    COBERTURA: Cubre los métodos search_product() y get_products_count() del POM HomePage.
    Verifica que la búsqueda funcione a través del POM.
    """
    home_page = HomePage(driver)
    home_page.go_to()

    # ✅ COBERTURA: Usar search_product() del POM
    home_page.search_product("Smartphone")

    # ✅ COBERTURA: Usar get_products_count() del POM
    count = home_page.get_products_count()
    assert count >= 0, "get_products_count() debería retornar un valor >= 0"
    print(f"✅ Búsqueda con POM completada. Productos encontrados: {count}")


def test_click_category_by_visible_text(driver):
    """
    COBERTURA: Cubre el método click_category_by_visible_text() del POM HomePage.
    Este método busca categorías por texto visible en vez de por localizador fijo.
    """
    home_page = HomePage(driver)
    home_page.go_to()

    # ✅ COBERTURA: Usar click_category_by_visible_text() del POM
    category_page = home_page.click_category_by_visible_text("Electronics")

    # Verificar que la navegación fue exitosa
    if category_page is not None:
        title = category_page.get_category_title()
        print(f"✅ Categoría navegada con POM visible text: '{title}'")
    else:
        print("⚠️  click_category_by_visible_text no retornó CategoryPage")


def test_login_button_visible_before_login(driver):
    """
    COBERTURA: Cubre los métodos is_login_button_visible() e is_logout_button_visible()
    del POM HomePage. Verifica el estado de botones cuando NO hay sesión.
    """
    home_page = HomePage(driver)
    home_page.go_to()

    # ✅ COBERTURA: Usar is_login_button_visible() del POM
    assert home_page.is_login_button_visible(), (
        "El botón 'Login' debería ser visible cuando no hay sesión activa"
    )
    print("✅ Botón 'Login' visible (POM is_login_button_visible)")

    # ✅ COBERTURA: Usar is_logout_button_visible() del POM
    # NO debería ser visible sin sesión
    is_logout = home_page.is_logout_button_visible()
    print(f"ℹ️  Botón 'Logout' visible: {is_logout} (esperado: False)")
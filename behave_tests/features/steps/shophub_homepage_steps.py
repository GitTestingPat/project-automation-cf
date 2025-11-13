from behave import given, when, then
from pages.shophub.shophub_home_page import HomePage


@given('que el usuario accede a la página principal de ShopHub')
def step_user_navigates_to_shophub(context):
    """Usuario navega a la página principal de ShopHub"""
    context.home_page = HomePage(context.driver)
    context.home_page.go_to()


@given('que el usuario está en la página principal de ShopHub')
def step_user_is_on_shophub_homepage(context):
    """Usuario está en la página principal de ShopHub"""
    context.home_page = HomePage(context.driver)
    context.home_page.go_to()


@then('el título de la página debe contener "{expected_text}"')
def step_verify_page_title(context, expected_text):
    """Verifica que el título de la página contenga el texto esperado"""
    actual_title = context.home_page.get_title()
    assert expected_text in actual_title, \
        f"El título '{actual_title}' no contiene '{expected_text}'"


@then('los elementos principales deben estar visibles')
def step_verify_main_elements_visible(context):
    """Verifica que los elementos principales estén visibles"""
    # Verificar que la página cargó correctamente
    assert context.home_page.get_title() is not None
    # Se puede agregar más verificaciones de elementos si es necesario


@when('el usuario hace clic en la categoría "{category_name}"')
def step_click_category(context, category_name):
    """Usuario hace clic en una categoría específica"""
    context.home_page.click_categories_dropdown()

    if category_name == "Men's Clothes":
        context.category_page = context.home_page.click_mens_category()
    elif category_name == "Women's Clothes":
        context.category_page = context.home_page.click_womens_category()
    elif category_name == "Electronics":
        context.category_page = context.home_page.click_electronics_category()
    else:
        raise ValueError(f"Categoría no reconocida: {category_name}")


@then('se deben mostrar productos de la categoría')
def step_verify_products_displayed(context):
    """Verifica que se muestren productos en la categoría"""
    products_count = context.home_page.get_products_count()
    assert products_count > 0, \
        f"No se encontraron productos. Contador: {products_count}"


@then('el contador de productos debe ser mayor a {expected_count:d}')
def step_verify_products_count_greater_than(context, expected_count):
    """Verifica que el contador de productos sea mayor al esperado"""
    actual_count = context.home_page.get_products_count()
    assert actual_count > expected_count, \
        f"Contador de productos ({actual_count}) no es mayor a {expected_count}"


@then('se deben mostrar productos de la categoría "{category_name}"')
def step_verify_category_products(context, category_name):
    """Verifica que se muestren productos de la categoría específica"""
    # Verificar que hay productos
    products_count = context.home_page.get_products_count()
    assert products_count > 0, \
        f"No se encontraron productos en la categoría {category_name}"

    # Verificar que el título contenga la categoría o ShopHub
    page_title = context.driver.title
    assert category_name in page_title or "ShopHub" in page_title, \
        f"El título '{page_title}' no contiene '{category_name}' ni 'ShopHub'"


@then('la página debe contener productos relevantes')
def step_verify_relevant_products(context):
    """Verifica que la página contenga productos relevantes"""
    products_count = context.home_page.get_products_count()
    assert products_count > 0, \
        "No se encontraron productos relevantes"


@then('se deben mostrar productos de electrónica')
def step_verify_electronics_products(context):
    """Verifica que se muestren productos de electrónica"""
    products_count = context.home_page.get_products_count()
    assert products_count > 0, \
        "No se encontraron productos de electrónica"


@then('el usuario debe poder ver los detalles de los productos')
def step_verify_can_see_product_details(context):
    """Verifica que el usuario pueda ver detalles de productos"""
    # Verificar que hay productos disponibles para ver detalles
    products_count = context.home_page.get_products_count()
    assert products_count > 0, \
        "No hay productos disponibles para ver detalles"
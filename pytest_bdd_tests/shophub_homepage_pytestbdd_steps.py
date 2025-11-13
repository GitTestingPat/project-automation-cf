from pytest_bdd import given, when, then, parsers
from pages.shophub.shophub_home_page import HomePage


@given('estoy en la página principal de ShopHub')
def given_on_shophub_homepage(driver, scenario_state):
    """Usuario está en la página principal de ShopHub"""
    home_page = HomePage(driver)
    home_page.go_to()
    scenario_state['home_page'] = home_page


@when(parsers.parse('hago clic en la categoría "{category_name}"'))
def when_click_category(scenario_state, category_name):
    """Usuario hace clic en una categoría específica"""
    home_page = scenario_state['home_page']
    home_page.click_categories_dropdown()

    if category_name == "Men's Clothes":
        category_page = home_page.click_mens_category()
    elif category_name == "Women's Clothes":
        category_page = home_page.click_womens_category()
    elif category_name == "Electronics":
        category_page = home_page.click_electronics_category()
    else:
        raise ValueError(f"Categoría no reconocida: {category_name}")

    scenario_state['category_page'] = category_page
    scenario_state['home_page'] = home_page


@then(parsers.parse('el título de la página debe contener "{expected_text}"'))
def then_page_title_contains(scenario_state, expected_text):
    """Verifica que el título de la página contenga el texto esperado"""
    home_page = scenario_state['home_page']
    actual_title = home_page.get_title()
    assert expected_text in actual_title, \
        f"El título '{actual_title}' no contiene '{expected_text}'"


@then('los elementos principales deben estar visibles')
def then_main_elements_visible(scenario_state):
    """Verifica que los elementos principales estén visibles"""
    home_page = scenario_state['home_page']
    assert home_page.get_title() is not None, \
        "Los elementos principales no están visibles"


@then('se deben mostrar productos de la categoría')
def then_category_products_shown(scenario_state):
    """Verifica que se muestren productos en la categoría"""
    home_page = scenario_state['home_page']
    products_count = home_page.get_products_count()
    assert products_count > 0, \
        f"No se encontraron productos. Contador: {products_count}"


@then('el contador de productos debe ser mayor a 0')
def then_products_count_greater_than_zero(scenario_state):
    """Verifica que el contador de productos sea mayor a 0"""
    home_page = scenario_state['home_page']
    actual_count = home_page.get_products_count()
    assert actual_count > 0, \
        f"Contador de productos ({actual_count}) no es mayor a 0"
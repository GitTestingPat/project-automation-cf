from behave import given, when, then
from selenium.webdriver.common.by import By
from pages.shophub.shophub_home_page import HomePage


@when('el usuario busca el producto "{search_term}"')
def step_user_searches_product(context, search_term):
    """Usuario busca un producto específico"""
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(context.driver)
        context.home_page.go_to()

    context.search_term = search_term
    context.home_page.search_product(search_term)


@when('el usuario ingresa texto en el campo de búsqueda')
def step_user_enters_text_in_search(context):
    """Usuario ingresa texto en el campo de búsqueda"""
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(context.driver)
        context.home_page.go_to()

    context.search_term = "Test Product"
    context.home_page.search_product(context.search_term)


@when('el usuario busca el término "{search_term}"')
def step_user_searches_term(context, search_term):
    """Usuario busca un término específico"""
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(context.driver)
        context.home_page.go_to()

    context.search_term = search_term
    context.home_page.search_product(search_term)


@then('el campo de búsqueda debe contener el texto "{expected_text}"')
def step_verify_search_field_contains_text(context, expected_text):
    """Verifica que el campo de búsqueda contenga el texto esperado"""
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input_element = context.driver.find_element(*SEARCH_INPUT)
    actual_value = search_input_element.get_attribute("value")

    assert actual_value == expected_text, \
        f"El campo de búsqueda no contiene '{expected_text}'. Valor actual: '{actual_value}'"


@then('el sistema debe haber procesado la búsqueda')
def step_verify_search_processed(context):
    """Verifica que el sistema haya procesado la búsqueda"""
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input_element = context.driver.find_element(*SEARCH_INPUT)

    # Verificar que el campo existe y tiene valor
    assert search_input_element is not None, "El campo de búsqueda no existe"
    assert search_input_element.get_attribute("value") != "", \
        "El campo de búsqueda está vacío"


@then('el campo debe reflejar el texto ingresado')
def step_verify_field_reflects_text(context):
    """Verifica que el campo refleje el texto ingresado"""
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input_element = context.driver.find_element(*SEARCH_INPUT)
    actual_value = search_input_element.get_attribute("value")

    assert actual_value == context.search_term, \
        f"El campo no refleja el texto ingresado. Esperado: '{context.search_term}', Actual: '{actual_value}'"


@then('el campo de búsqueda debe estar funcional')
def step_verify_search_field_functional(context):
    """Verifica que el campo de búsqueda esté funcional"""
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input_element = context.driver.find_element(*SEARCH_INPUT)

    # Verificar que el campo está visible y habilitado
    assert search_input_element.is_displayed(), \
        "El campo de búsqueda no está visible"
    assert search_input_element.is_enabled(), \
        "El campo de búsqueda no está habilitado"


@then('el sistema debe mostrar resultados relacionados con "{search_term}"')
def step_verify_search_results_related_to_term(context, search_term):
    """Verifica que el sistema muestre resultados relacionados con el término buscado"""
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input_element = context.driver.find_element(*SEARCH_INPUT)

    # Verificar que la búsqueda se realizó
    assert search_input_element.get_attribute("value") == search_term, \
        f"El campo de búsqueda no contiene '{search_term}'"
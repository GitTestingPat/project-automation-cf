from selenium.webdriver.common.by import By
from pages.shophub.shophub_home_page import HomePage


def test_search_input_accepts_text(driver):
    """
    TC-WEB-11: Verificar que el campo de búsqueda acepta texto.
    La prueba valida que el campo de búsqueda esté presente y funcional dentro de la UI.
    """
    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Buscar un término cualquiera
    search_term = "Electronics"
    home_page.search_product(search_term)

    # 3. Verificar que el campo de búsqueda contiene el texto (feedback visual para el usuario)
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input_element = driver.find_element(*SEARCH_INPUT)

    assert search_input_element.get_attribute("value") == search_term, \
        f"El campo de búsqueda no contiene el texto '{search_term}' después de enviarlo."

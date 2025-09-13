import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.shophub_home_page import HomePage

def test_search_product_by_nonexistent_name(driver):
    """
    TC-WEB-12: Buscar producto por nombre inexistente.
    Dado que la tienda de prueba no tiene funcionalidad de búsqueda implementada,
    esta prueba valida que el campo de búsqueda acepte cualquier texto sin errores,
    y que la página no se rompa al realizar la búsqueda.
    """
    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Buscar un producto que definitivamente no existe
    nonexistent_term = "XyZ123_NoExiste_@#!"
    home_page.search_product(nonexistent_term)

    # 3. Verificar que el campo de búsqueda contiene el texto inexistente
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input_element = driver.find_element(*SEARCH_INPUT)

    assert search_input_element.get_attribute("value") == nonexistent_term, \
        f"El campo de búsqueda no contiene el texto inexistente '{nonexistent_term}'."

    # 4. Verificar que la página sigue siendo funcional: Esperar a que un elemento clave sea visible
    try:
        # Esperar hasta 10 segundos a que el título "Shop by Category" sea visible
        category_title_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Shop by Category']"))
        )
        assert category_title_element.is_displayed(), "El título 'Shop by Category' no es visible."
    except Exception:
        pytest.fail("El título 'Shop by Category' no se volvió a mostrar tras la búsqueda. "
                    "La página puede haberse roto.")
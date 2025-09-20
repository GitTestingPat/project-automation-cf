import pytest
from pages.fake_cinema.cinema_home_page import CinemaHomePage

def test_add_food_to_cart(driver):
    """
       TC-WEB-28: Selección de comida adicional
    """
    # Arrange
    home_page = CinemaHomePage(driver)

    # Act
    home_page.go_to()
    home_page.click_food_tab()
    home_page.click_first_food_item()
    home_page.click_add_to_cart_button()

    # La prueba DEBE FALLAR porque is_cart_updated() siempre retorna False
    assert home_page.is_cart_updated(), "El carrito debería haberse actualizado, pero el botón no hace nada."
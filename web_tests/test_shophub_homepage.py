from pages.shophub_home_page import HomePage
import pytest


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
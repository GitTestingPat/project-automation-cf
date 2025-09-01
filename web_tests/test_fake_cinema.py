from selenium import webdriver
import pytest
from pages.cinema_home_page import CinemaHomePage

'''
Prueba TC-WEB-13 Verificar título principal
'''

def test_homepage_has_hero_text():
    driver = webdriver.Chrome()
    home_page = CinemaHomePage(driver)

    home_page.go_to()
    hero_text = home_page.get_hero_text()

    assert "héroe" in hero_text.lower()

    driver.quit()
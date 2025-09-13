import pytest
from pages.fake_cinema.cinema_home_page import CinemaHomePage

'''
Prueba TC-WEB-14 Verificar descripción de la película
'''

def test_navigate_to_movie_detail_and_verify_title(driver):

    home_page = CinemaHomePage(driver)
    expected_movie_title = "Los 4 Fantásticos: Primeros Pasos"


    home_page.go_to()
    home_page.navigate_to_movie_detail()
    actual_title = home_page.get_movie_detail_title()

    assert expected_movie_title == actual_title, \
        f"El título esperado no coincide. Obtenido: {actual_title}"
import pytest
from pages.fake_cinema.cinema_home_page import CinemaHomePage

def test_verify_home_page_access(driver):
    """
    TC-WEB-15: Verificación del Acceso a la Página Principal
    - Descripción: Comprobar que el usuario puede acceder correctamente a la página principal.
    - Resultado esperado: La página se carga mostrando el título principal
    """
    # Arrange
    home_page = CinemaHomePage(driver)
    expected_hero_title = "¡El mismo héroe, como nunca antes!"

    # Act
    home_page.go_to()
    actual_hero_title = home_page.get_hero_text()

    # Assert
    assert actual_hero_title == expected_hero_title, \
        f"Título del hero no coincide. Esperado: '{expected_hero_title}', Obtenido: '{actual_hero_title}'"
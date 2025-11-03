from pages.fake_cinema.cinema_home_page import CinemaHomePage

def test_select_movie_from_billboard(driver):
    """
    TC-WEB-16: Selección de Película desde la Cartelera
    - Descripción: Validar que el usuario pueda seleccionar 'Jurassic World: Renace' desde la cartelera.
    - Resultado esperado: Se redirige al detalle de la película y muestra su título.
    """
    # Arrange
    home_page = CinemaHomePage(driver)
    expected_movie_title = "Jurassic World: Renace"

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    actual_title = home_page.get_movie_detail_title()

    # Assert
    assert expected_movie_title in actual_title, \
        f"El título de la película no coincide. Esperado: '{expected_movie_title}', Obtenido: '{actual_title}'"
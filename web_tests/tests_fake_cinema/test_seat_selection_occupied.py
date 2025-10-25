import pytest
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_cannot_select_occupied_seat(driver):
    """
    TC-WEB-41: Intento de Selección de Asiento Ocupado
    - Descripción: Validar que el usuario NO pueda seleccionar un asiento ya ocupado.
    - Resultado esperado: El asiento ocupado está presente y deshabilitado; no se marca como seleccionado.
    """
    # Arrange
    home_page = CinemaHomePage(driver)

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_date("26") # Ajustar según disponibilidad real
    home_page.select_first_available_time()

    # Solo verificar que exista un asiento ocupado
    occupied_seat = home_page.get_first_occupied_seat()

    # Assert
    assert not occupied_seat.is_enabled(), \
        "El asiento ocupado debe estar deshabilitado."

    print("\n[INFO] Asiento ocupado verificado como no seleccionable.")
    print("[INFO] ¡Prueba EXITOSA! El asiento tiene el atributo 'disabled'.")
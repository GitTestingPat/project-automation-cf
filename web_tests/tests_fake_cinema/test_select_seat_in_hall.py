import pytest
from pages.fake_cinema.cinema_home_page import CinemaHomePage

def test_select_seat_in_hall(driver):
    """
    TC-WEB-18: Selección de Asiento en la Sala
    - Descripción: Validar que el usuario pueda seleccionar un asiento disponible.
    - Resultado esperado: El asiento se marca como seleccionado (se verifica por presencia de '80' en pantalla).
    """
    # Arrange
    home_page = CinemaHomePage(driver)

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_date("17") # Ajustar según disponibilidad real
    home_page.select_first_available_time()
    selected_seat = home_page.select_first_available_seat()

    # Assert
    assert home_page.is_seat_selected(), \
        "El asiento no se marcó como seleccionado después de hacer clic."

    print(f"\n[INFO] Asiento seleccionado: {selected_seat}")
    print("[INFO] ¡Prueba EXITOSA! Se detectó '80' en pantalla, indicando que el asiento fue seleccionado.")
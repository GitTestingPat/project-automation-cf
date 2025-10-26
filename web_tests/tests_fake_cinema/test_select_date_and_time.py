import pytest
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_select_date_and_time(driver):
    """
    TC-WEB-17: Selección de Fecha y Hora de Proyección
    - Descripción: Verificar que el usuario pueda elegir una fecha y la primera hora disponible.
    - Resultado esperado: El sistema muestra la sala disponible y los asientos libres.
    """
    # Arrange
    home_page = CinemaHomePage(driver)
    target_date = "27" # Ajustar según disponibilidad real

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_date(target_date)

    # Selecciona la primera hora disponible
    selected_time = home_page.select_first_available_time()

    # Assert
    assert home_page.is_seat_grid_displayed(), \
        "La cuadrícula de asientos no se cargó después de seleccionar fecha y hora."

    # Imprimir la hora seleccionada para debugging
    print(f"\n[INFO] Hora seleccionada dinámicamente: {selected_time}")
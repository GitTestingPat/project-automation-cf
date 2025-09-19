import pytest
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_select_multiple_seats(driver):
    """
    TC-WEB-26: Selección de Múltiples Asientos
    - Descripción: Validar que el usuario pueda seleccionar múltiples asientos disponibles.
    - Resultado esperado: Los asientos se marcan como seleccionados y el precio total refleja la suma correcta
    (ej. 3 x $80 = $240).
    TC-WEB-27: Cancelación de Asientos Seleccionados
    """
    # Arrange
    home_page = CinemaHomePage(driver)
    expected_seat_count = 3
    expected_total_price = 80 * expected_seat_count  # $240

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_date("20")  # La fecha debe cambiar cada vez que se corre la prueba
    home_page.select_first_available_time()

    print(f"[DEBUG] Seleccionando {expected_seat_count} asientos...")
    selected_seats = home_page.select_multiple_seats(expected_seat_count)

    print(f"[DEBUG] Asientos seleccionados: {selected_seats}")

    # Assert
    # Verificar que se seleccionaron exactamente la cantidad esperada
    assert len(selected_seats) == expected_seat_count, \
        f"Se esperaban {expected_seat_count} asientos seleccionados, pero se seleccionaron {len(selected_seats)}."

    # Verificar que el precio total refleja la suma correcta
    # Buscar CUALQUIER elemento que contenga el texto del precio total esperado
    assert home_page.is_total_price_displayed(expected_total_price), \
        f"No se encontró el precio total esperado de ${expected_total_price} en la pantalla."

    print(f"\n[INFO] Asientos seleccionados: {selected_seats}")
    print(f"[INFO] Precio total esperado: ${expected_total_price} detectado correctamente.")
    print("[INFO] ¡Prueba PASADA! Múltiples asientos seleccionados y precio total verificado.")
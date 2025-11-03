from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import CinemaHomePage


def test_navigate_to_movie_detail_and_verify_title(driver):
    """
    TC-WEB-14: Verificar información de película (CORREGIDO USANDO POM)
    """
    home_page = CinemaHomePage(driver)
    expected_movie_title = "Los 4 Fantásticos: Primeros Pasos"

    # Act
    home_page.go_to()

    # Usar método navigate_to_movie_detail() del POM (línea 277-281)
    home_page.navigate_to_movie_detail(home_page.FANTASTIC_FOUR_DETAIL_BUTTON)

    # Esperar que cargue (usando localizador MOVIE_DETAIL_TITLE del POM)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(home_page.MOVIE_DETAIL_TITLE)
    )

    # Usar método get_movie_detail_title() del POM (línea 283-287)
    actual_title = home_page.get_movie_detail_title()

    # Assert - Validaciones usando SOLO métodos del POM

    # 1. Validar título
    assert expected_movie_title == actual_title, \
        f"Título no coincide. Esperado: '{expected_movie_title}', Obtenido: '{actual_title}'"
    print(f"✅ Título validado: {actual_title}")

    # 2. Seleccionar fecha usando método select_first_available_date() del POM (línea 301-334)
    home_page.select_first_available_date()
    print(f"✅ Fecha seleccionada correctamente")

    # 3. Seleccionar hora usando método select_first_available_time() del POM (línea 336-364)
    selected_time = home_page.select_first_available_time()
    assert selected_time is not None, "No se pudo seleccionar horario"
    assert ":" in selected_time, f"Formato de hora inválido: {selected_time}"
    print(f"✅ Horario seleccionado: {selected_time}")

    # 4. Verificar que se cargó la sala usando método is_seat_grid_displayed() del POM (línea 366-385)
    assert home_page.is_seat_grid_displayed(), "La sala de asientos no se cargó correctamente"
    print(f"✅ Sala de asientos cargada correctamente")

    print(f"✅ Información completa de película validada")
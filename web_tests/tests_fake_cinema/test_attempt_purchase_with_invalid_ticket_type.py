import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import CinemaHomePage


def test_attempt_purchase_with_invalid_ticket_type(driver):
    """
    TC-WEB-36: Intento de compra con tipo de boleto inválido, seleccionando un solo asiento
    El sistema debe mostrar un mensaje de error: "La cantidad debe coincidir con los asientos seleccionados".
    El botón "Confirmar" permanece inactivo hasta que se ingrese un valor válido.
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba de validación de tarjeta inválida...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha...")
        home_page.select_first_available_date()
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time()
        print("[DEBUG] Seleccionando primer asiento disponible...")
        home_page.select_first_available_seat()

        # Esperar y hacer clic en "Comprar boletos"
        print("[DEBUG] Esperando que el botón 'Comprar boletos' esté clickeable...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        home_page.click_buy_tickets_button()

        # Esperar modal y click en confirmar selección de boletos
        print("[DEBUG] Esperando modal de selección de boletos...")
        home_page.wait_for_ticket_modal()
        print("[DEBUG] Confirmando selección de boletos...")
        home_page.confirm_tickets_selection()

        # Verificar mensaje de error
        print("[DEBUG] Confirmando el mensaje: 'La cantidad debe coincidir con los asientos seleccionados'")
        home_page.confirm_error_message()

        # Verificar que el botón "Confirmar" esté inactivo
        print("[DEBUG] Verificando que el botón 'Confirmar' esté inactivo...")
        home_page.is_confirm_button_disabled()

    except Exception as e:
        pytest.fail(f"La prueba falló: {str(e)}")
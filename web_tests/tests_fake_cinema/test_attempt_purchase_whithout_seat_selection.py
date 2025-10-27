import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
import time


def test_attempt_purchase_whithout_seat_selection(driver):
    """
    TC-WEB-35: Intento de Compra sin Selección de Asiento
    La prueba que el botón "Comprar boletos" debe estar deshabilitado.
    O bien, al intentar hacer clic, aparece un mensaje de error: "Por favor, seleccione al menos un asiento".
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba de validación de email inválido...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha...")
        home_page.select_date("28")  # Ajustar según disponibilidad real
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time()

        # Esperar y hacer clic en "Comprar boletos"
        print("[DEBUG] Verificando que el botón 'Comprar boletos' esté deshabilitado inicialmente...")
        buy_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(home_page.BUY_TICKETS_BUTTON)
        )

        # Verificar que el botón esté deshabilitado (por atributo 'disabled' o por clase CSS)
        # Opción 1: Verificar atributo 'disabled'
        is_disabled = buy_button.get_attribute("disabled") is not None
        # Verificar clase 'disabled':

        assert is_disabled, ("El botón 'Comprar boletos' debería estar deshabilitado si no se han seleccionado "
                             "asientos.")

        print("[DEBUG] ✅ Botón correctamente deshabilitado sin selección de asientos.")

        # En caso de que el botón permita comprar boletos
        try:
            buy_button.click()
            print("[DEBUG] ⚠️ ¡Advertencia! Se permitió hacer clic en el botón deshabilitado.")
            # Fallar la prueba aquí si el clic es permitido
            pytest.fail("Se permitió hacer clic en el botón 'Comprar boletos' sin seleccionar asientos.")
        except Exception as e:
            print(f"[DEBUG] ✅ Clic bloqueado como se esperaba: {str(e)}")

        # --- UNA VERIFICACIÓN MÁS: Continuar seleccionando un asiento y verificar que se habilite ---
        print("[DEBUG] Seleccionando un asiento para habilitar el botón...")
        home_page.select_first_available_seat()

        print("[DEBUG] Esperando que el botón se habilite tras seleccionar asiento...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        # Verificar nuevamente que ahora NO esté deshabilitado
        buy_button_fresh = driver.find_element(*home_page.BUY_TICKETS_BUTTON)
        is_now_enabled = buy_button_fresh.get_attribute("disabled") is None
        assert is_now_enabled, "El botón debería estar habilitado después de seleccionar un asiento."

        print("[DEBUG] ✅ Botón correctamente habilitado tras seleccionar asiento.")

    except Exception as e:
        pytest.fail(f"La prueba falló con la excepción: {str(e)}")
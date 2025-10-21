import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_confirm_ticket_type(driver):
    """
    TC-WEB-19: Confirmación de Tipo de Boleto
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando fecha")
        home_page.select_date("22") # Ajustar según disponibilidad real
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time()
        print("[DEBUG] Seleccionando primer asiento disponible...")
        home_page.select_first_available_seat()

        # Verificar que el botón "Comprar boletos" ahora está habilitado
        buy_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        print("[DEBUG] Botón 'Comprar boletos' está habilitado.")

        # Esperar explícitamente al botón "Comprar boletos" después de seleccionar asiento
        print("[DEBUG] Esperando que el botón 'Comprar boletos' esté clickeable...")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )
        print("[DEBUG] Botón 'Comprar boletos' listo.")

        print("[DEBUG] Clic en 'Comprar boletos'...")
        home_page.click_buy_tickets_button()

        print("[DEBUG] espera a que 'Modal esté visible'...")
        home_page.wait_for_ticket_modal()

        print("[DEBUG] Seleccionando 1 boleto adulto...")
        home_page.select_adult_ticket(quantity=1)

        print("[DEBUG] Seleccionando 1 boleto adulto mayor...")
        home_page.select_senior_ticket(quantity=1)

        print("[DEBUG] Clic en 'Confirmar'...")
        home_page.confirm_tickets_selection()

        print("[INFO] ¡Prueba completada con éxito!")

    except Exception as e:
        print(f"[CRITICAL] Error durante la prueba TC-WEB-19: {str(e)}")
        raise  # Re-lanza la excepción para que pytest la marque como fallida

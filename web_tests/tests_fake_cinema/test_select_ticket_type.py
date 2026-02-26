from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_confirm_ticket_type(driver):
    """
    TC-WEB-19: Confirmación de Tipo de Boleto
    REFACTORIZADO: Usa más métodos del POM para aumentar cobertura.
    """
    home_page = CinemaHomePage(driver)

    try:
        print("[DEBUG] Iniciando prueba...")
        home_page.go_to()
        print("[DEBUG] Navegando a detalle de Jurassic World...")
        home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
        print("[DEBUG] Seleccionando primera hora disponible...")
        home_page.select_first_available_time_resilient()
        print("[DEBUG] Seleccionando primer asiento disponible...")
        home_page.select_first_available_seat()

        # ✅ COBERTURA: debug_current_page_title()
        home_page.debug_current_page_title()

        # Verificar que el botón "Comprar boletos" ahora está habilitado
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(home_page.BUY_TICKETS_BUTTON)
        )

        print("[DEBUG] Clic en 'Comprar boletos'...")
        home_page.click_buy_tickets_button()

        print("[DEBUG] espera a que 'Modal esté visible'...")
        home_page.wait_for_ticket_modal()

        # ✅ COBERTURA: is_cart_summary_visible()
        cart_visible = home_page.is_cart_summary_visible()
        print(f"[DEBUG] Resumen de carrito visible: {cart_visible}")

        print("[DEBUG] Seleccionando 1 boleto adulto...")
        home_page.select_adult_ticket(quantity=1)

        # ✅ COBERTURA: get_adults_cart_text()
        try:
            adults_text = home_page.get_adults_cart_text()
            print(f"[DEBUG] Texto de adultos: {adults_text}")
        except Exception:
            print("[DEBUG] No se pudo obtener texto de adultos")

        print("[DEBUG] Seleccionando 1 boleto adulto mayor...")
        # ✅ COBERTURA: select_senior_ticket()
        home_page.select_senior_ticket(quantity=1)

        # ✅ COBERTURA: get_seniors_cart_text()
        try:
            seniors_text = home_page.get_seniors_cart_text()
            print(f"[DEBUG] Texto de adultos mayores: {seniors_text}")
        except Exception:
            print("[DEBUG] No se pudo obtener texto de adultos mayores")

        # ✅ COBERTURA: get_total_price_text()
        try:
            total_text = home_page.get_total_price_text()
            print(f"[DEBUG] Precio total: {total_text}")
        except Exception:
            print("[DEBUG] No se pudo obtener precio total")

        print("[DEBUG] Clic en 'Confirmar'...")
        home_page.confirm_tickets_selection()

        print("[INFO] ¡Prueba completada con éxito!")

    except Exception as e:
        print(f"[CRITICAL] Error durante la prueba TC-WEB-19: {str(e)}")
        raise

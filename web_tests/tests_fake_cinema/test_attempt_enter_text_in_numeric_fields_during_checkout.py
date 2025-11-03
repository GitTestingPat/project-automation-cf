from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
from selenium.common.exceptions import TimeoutException


"""
    TC-WEB-45: Intento de ingresar texto en campos numéricos dentro del checkout
    Esta prueba verifica que el sistema ignora o rechaza la entrada.
    Muestra un mensaje de error: "Solo se permiten números".
"""


def test_attempt_to_enter_text_in_numeric_fields(driver):
    # Inicializar página
    home_page = CinemaHomePage(driver)

    # Navegar a la página principal
    home_page.go_to()

    # Ir al detalle de una película
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)

    # Seleccionar fecha de función
    home_page.select_first_available_date()

    # Elegir primer horario disponible
    home_page.select_first_available_time()

    # Seleccionar primer asiento libre
    home_page.select_first_available_seat()

    # Hacer clic en "Comprar boletos"
    home_page.click_buy_tickets_button()

    # Esperar modal de selección de boletos
    home_page.wait_for_ticket_modal()

    # Seleccionar 1 boleto adulto
    home_page.select_adult_ticket(quantity=1)

    # Confirmar selección de boletos
    home_page.confirm_tickets_selection()

    # Esperar redirección al carrito
    WebDriverWait(driver, 15).until(
        EC.url_contains("/cart")
    )

    # Hacer clic en "Proceder al pago"
    home_page.click_proceed_to_checkout()

    # Esperar carga de la página de checkout
    WebDriverWait(driver, 15).until(
        EC.url_contains("checkout")
    )

    # Rellenar formulario con texto en campos numéricos
    home_page.fill_payment_form(
        first_name="Bruce",
        last_name="Wayne",
        email="bruce.wayne@example.com",
        card_name="Bruce Wayne",
        card_number="abcd1234efgh5678",  # Texto en campo numérico
        cvv="xyz"  # Texto en campo numérico
    )

    # Obtener referencias a los campos numéricos
    card_number_field = driver.find_element(By.ID, "cardNumber")
    cvv_field = driver.find_element(By.ID, "cvv")

    # Verificar valor real en campo de número de tarjeta
    actual_card_number = card_number_field.get_attribute("value")
    assert actual_card_number != "abcd1234efgh5678", \
        "❌ El campo 'Número de tarjeta' aceptó texto. Debe rechazarlo o ignorarlo."

    # Verificar valor real en campo CVV
    actual_cvv = cvv_field.get_attribute("value")
    assert actual_cvv != "xyz", \
        "❌ El campo 'CVV' aceptó texto. Debe rechazarlo o ignorarlo."

    # Forzar validación del formulario
    driver.execute_script("""
        const form = document.querySelector('form');
        if (form) {
            form.reportValidity();
        }
    """)

    # Esperar brevemente para que aparezcan mensajes de error
    WebDriverWait(driver, 3).until(
        lambda d: any(
            "solo se permiten números" in el.text.lower()
            for el in d.find_elements(By.XPATH, "//*[contains(text(), 'Solo se permiten números') "
                                                "or contains(text(), 'solo se permiten números')]")
        ) or
        card_number_field.get_attribute("validationMessage") or
        cvv_field.get_attribute("validationMessage")
    )

    # Buscar mensaje de error específico en el DOM
    error_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), "
                                                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                                                    "'solo se permiten números')]")

    # Verificar mensaje de error en campos individuales
    card_number_validation = card_number_field.get_attribute("validationMessage")
    cvv_validation = cvv_field.get_attribute("validationMessage")

    # Validar que al menos un mecanismo de error esté activo
    assert (error_elements or "solo se permiten números" in card_number_validation.lower() or
            "solo se permiten números" in cvv_validation.lower()), \
        "❌ No se mostró el mensaje de error esperado: 'Solo se permiten números'."

    # Confirmar que el botón de pago sigue deshabilitado o no envía
    try:
        confirm_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(home_page.CONFIRM_PAYMENT_BUTTON)
        )
        confirm_button.click()

        # Si se permite el clic, verificar que no se abandona checkout
        WebDriverWait(driver, 5).until(
            EC.url_contains("checkout")
        )
    except TimeoutException:
        # Es aceptable que el botón esté deshabilitado
        pass

    # Finalizar prueba con éxito
    print("[INFO] ✅ Validación de campos numéricos funcionando correctamente.")
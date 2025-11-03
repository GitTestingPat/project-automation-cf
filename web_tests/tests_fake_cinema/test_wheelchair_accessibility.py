from selenium.webdriver.common.by import By
from pages.fake_cinema.cinema_home_page import CinemaHomePage

def test_wheelchair_accessibility_button(driver):
    """
    TC-WEB-31: Verifica que se pueda hacer clic en el icono de "Silla de ruedas" en la sala.
    La prueba debe fallar porque el botón del icono de silla de ruedas no hace nada.
    """

    print("\n[TEST START] Iniciando prueba de accesibilidad: ¿El botón de silla de ruedas da feedback al usuario?")

    home_page = CinemaHomePage(driver)
    home_page.go_to()
    home_page.click_movie_card()
    home_page.click_showtime_button()

    # Localizar el botón ANTES del clic
    wheelchair_button_locator = (
        By.CSS_SELECTOR,
        'div:nth-of-type(4) > button.hover\\:bg-accent'
    )
    button_before = driver.find_element(*wheelchair_button_locator)

    # Capturar atributos o clases relevantes ANTES del clic
    classes_before = button_before.get_attribute("class")
    print(f"[DEBUG] Clases del botón ANTES del clic: {classes_before}")

    # Clic en botón silla de ruedas
    home_page.click_wheelchair_icon()

    # Volver a localizar el botón DESPUÉS del clic
    button_after = driver.find_element(*wheelchair_button_locator)
    classes_after = button_after.get_attribute("class")
    print(f"[DEBUG] Clases del botón DESPUÉS del clic: {classes_after}")

    # ✅ Verificar si hubo algun cambio observable para el usuario
    # Esto incluye: cambio de clase, estilo, aparición de tooltip, modal, etc.
    if classes_before == classes_after:
        # 🚫 ¡ALERTA! El botón no cambió visualmente → el usuario no sabe que su clic fue registrado.
        assert False, (
            "BUG DE ACCESIBILIDAD: El botón de silla de ruedas NO proporciona feedback visual ni funcionalidad. "
            "Tras hacer clic, no cambió su estado, clase, ni apariencia. "
            "Para el usuario, es como si el botón estuviera roto o no hiciera nada. "
            "Esto es inaceptable en una interfaz accesible."
        )
    else:
        print("[TEST PASSED] ✅ El botón cambió su estado/apariencia. El usuario recibe feedback visual.")

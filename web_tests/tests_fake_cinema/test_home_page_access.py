from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_verify_home_page_access(driver):
    """
    TC-WEB-15: Verificación del Acceso a la Página Principal
    """
    home_page = CinemaHomePage(driver)
    expected_hero_title = "¡El mismo héroe, como nunca antes!"

    # Act
    home_page.go_to()

    # Espera explícita para el título (usando HERO_TITLE que YA existe)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(home_page.HERO_TITLE)
    )

    actual_hero_title = home_page.get_hero_text()

    # Assert - Validaciones mejoradas usando elementos REALES

    # 1. Validar título principal
    assert actual_hero_title == expected_hero_title, \
        f"Título no coincide. Esperado: '{expected_hero_title}', Obtenido: '{actual_hero_title}'"

    # 2. Validar que los botones de "Ver detalle" están presentes
    # (usando FANTASTIC_FOUR_DETAIL_BUTTON y JURASSIC_WORLD_DETAIL_BUTTON que YA existen)
    fantastic_button = driver.find_element(*home_page.FANTASTIC_FOUR_DETAIL_BUTTON)
    assert fantastic_button.is_displayed(), "El botón de 'Los 4 Fantásticos' no está visible"

    jurassic_button = driver.find_element(*home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    assert jurassic_button.is_displayed(), "El botón de 'Jurassic World' no está visible"

    # 3. Validar que los botones son clickeables
    assert fantastic_button.is_enabled(), "El botón de 'Los 4 Fantásticos' no es clickeable"
    assert jurassic_button.is_enabled(), "El botón de 'Jurassic World' no es clickeable"

    # 4. Validar URL correcta
    assert "fake-cinema.vercel.app" in driver.current_url, \
        f"URL incorrecta: {driver.current_url}"

    # 5. Validar que la página no tiene errores 404/500
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "404" not in page_text, "La página contiene error 404"
    assert "500" not in page_text, "La página contiene error 500"

    print(f"✅ Página principal cargada correctamente")
    print(f"✅ Título: {actual_hero_title}")
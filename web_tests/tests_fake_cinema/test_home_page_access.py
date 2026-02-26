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

    # Assert - Validaciones usando POM

    # 1. Validar título principal
    assert actual_hero_title == expected_hero_title, \
        f"Título no coincide. Esperado: '{expected_hero_title}', Obtenido: '{actual_hero_title}'"

    # 2. Validar descripción del hero usando POM get_hero_description()
    hero_description = home_page.get_hero_description()
    assert hero_description is not None and hero_description != "", \
        "La descripción del hero está vacía"
    print(f"✅ Descripción del hero: {hero_description[:60]}...")

    # 3. Validar navegación a detalle de película usando POM navigate_to_movie_detail()
    home_page.navigate_to_movie_detail(home_page.FANTASTIC_FOUR_DETAIL_BUTTON)

    # 4. Validar título de la película usando POM get_movie_detail_title()
    movie_title = home_page.get_movie_detail_title()
    assert movie_title is not None and movie_title != "", \
        "El título de la película está vacío"
    assert "Fantásticos" in movie_title or "4" in movie_title, \
        f"Título de película inesperado: {movie_title}"
    print(f"✅ Título de película: {movie_title}")

    # 5. Validar URL correcta
    assert "fake-cinema.vercel.app" in driver.current_url, \
        f"URL incorrecta: {driver.current_url}"

    print(f"✅ Página principal cargada correctamente")
    print(f"✅ Título: {actual_hero_title}")
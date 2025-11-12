from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
import time

"""
    TC-WEB-43: Intento de cambiar de película sin confirmar la selección.
    El sistema redirige a la nueva película. El carrito se mantiene en estado vacío.
"""


def test_attempt_change_movie_without_confirming_selection(driver):
    home_page = CinemaHomePage(driver)

    print("[DEBUG] Navegando a la página principal del cine...")
    home_page.go_to()

    # Navegar a la primera película (Fantastic Four)
    print("[DEBUG] Navegando a Fantastic Four...")
    home_page.navigate_to_movie_detail(home_page.FANTASTIC_FOUR_DETAIL_BUTTON)
    print("[DEBUG] ✅ Fantastic Four seleccionada.")

    # Volver al listado de películas
    print("[DEBUG] Volviendo al listado de películas (clic en logo home)...")
    home_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/'][@class='text-2xl font-bold text-white']"))
    )
    driver.execute_script("arguments[0].click();", home_button)

    # Esperar que el listado esté disponible
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid"))
    )
    time.sleep(1)
    print("[DEBUG] ✅ Redirigido al listado de películas.")

    # Navegar a la segunda película (Jurassic World)
    print("[DEBUG] Navegando a Jurassic World...")
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    print("[DEBUG] ✅ Jurassic World seleccionada.")

    # Navegar al carrito
    print("[DEBUG] Navegando al carrito desde el menú...")
    cart_link = home_page.wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Carrito')]"))
    )
    cart_link.click()
    print("[DEBUG] ✅ Accedido al carrito.")

    # Verificar que el carrito esté vacío
    print("[DEBUG] Verificando que el carrito esté vacío...")
    cart_is_empty = not home_page.is_cart_summary_visible()
    assert cart_is_empty, "El carrito no debe contener ítems tras cambiar de película sin confirmar."
    print("[DEBUG] ✅ Carrito confirmado como vacío. Prueba exitosa.")
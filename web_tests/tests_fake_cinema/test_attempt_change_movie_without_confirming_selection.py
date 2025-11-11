from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.fake_cinema.cinema_home_page import CinemaHomePage
import time

"""
    TC-WEB-43: Intento de cambiar de película sin confirmar la selección.
    El sistema redirige a la nueva película. El carrito se mantiene en estado vacio.
"""


def test_attempt_change_movie_without_confirming_selection(driver):
    # Inicializar la página principal usando el Page Object Model
    home_page = CinemaHomePage(driver)

    # Navegar a la URL principal del cine
    print("[DEBUG] Navegando a la página principal del cine...")
    home_page.go_to()

    # Hacer clic en la cuarta película de la grilla (F1)
    print("[DEBUG] Haciendo clic en la cuarta película de la grilla...")
    fourth_movie = home_page.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.grid > div:nth-of-type(4) > div > a"))
    )
    fourth_movie.click()
    print("[DEBUG] ✅ Cuarta película seleccionada.")

    # Volver al listado de películas haciendo clic en el logo/home
    print("[DEBUG] Volviendo al listado de películas (clic en logo home)...")
    home_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/'][@class='text-2xl font-bold text-white']"))
    )
    driver.execute_script("arguments[0].click();", home_button)

    # Esperar que el listado de películas se cargue
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid > div:nth-of-type(5)"))
    )
    time.sleep(1)  # Espera adicional para estabilidad
    print("[DEBUG] ✅ Redirigido al listado de películas.")

    # RE-LOCALIZAR la quinta película después de la navegación (Toy Story)
    print("[DEBUG] Haciendo clic en la quinta película de la grilla...")
    fifth_movie = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.grid > div:nth-of-type(5) > div > a"))
    )
    time.sleep(0.5)  # Pequeña pausa antes del clic
    fifth_movie.click()
    print("[DEBUG] ✅ Quinta película seleccionada.")

    # Navegar al carrito desde el menú de navegación
    print("[DEBUG] Navegando al carrito desde el menú...")
    cart_link = home_page.wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Carrito')]"))
    )
    cart_link.click()
    print("[DEBUG] ✅ Accedido al carrito.")

    # Verificar que el carrito esté vacío (no se muestra resumen de compra)
    print("[DEBUG] Verificando que el carrito esté vacío...")
    cart_is_empty = not home_page.is_cart_summary_visible()
    assert cart_is_empty, "El carrito no debe contener ítems tras cambiar de película sin confirmar."
    print("[DEBUG] ✅ Carrito confirmado como vacío. Prueba exitosa.")
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.shophub.shophub_home_page import HomePage


def test_view_cart_content_as_logged_in_user(driver):
    """
    Caso de prueba: TC-WEB-10: Ver contenido del carrito
    Objetivo: Verificar que un usuario autenticado pueda ver el contenido de su carrito de compras.
    Esta prueba requiere un usuario autenticado y un producto agregado al carrito.
    """
    print("🔍 [1] Navegando a la página principal...")
    home_page = HomePage(driver)
    home_page.go_to()

    print("🔍 [2] Iniciando sesión...")
    login_page = home_page.click_login()
    login_page.enter_email("admin@demo.com")
    login_page.enter_password("SecurePass123!")
    login_page.click_sign_in()

    print("🔍 [3] Eliminando overlays de carga...")
    driver.execute_script(
        "document.querySelectorAll('div[role=\"status\"], .loading-overlay, .overlay, "
        ".spinner, [class*=\"loading\"], [class*=\"overlay\"]').forEach(el => el.remove());"
    )

    print("🔍 [4] Esperando desaparición del overlay...")
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[role='status']"))
    )
    print("✅ Overlay eliminado.")

    print("🔍 [5] Verificando página de 'Logged In'...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Logged In')]"))
    )
    print("✅ Página de confirmación detectada.")

    print("🔍 [6] Haciendo clic en 'Go to Home'...")
    go_to_home_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Go to Home']"))
    )
    go_to_home_btn.click()
    print("✅ Clic en 'Go to Home' realizado.")

    print("🔍 [7] Esperando que cargue la página principal (logo o menú)...")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//header//a[@href='/'] | //h1[contains(text(), 'ShopHub')]"))
    )
    print("✅ Página principal detectada.")

    print("🔍 [8] Verificando que el usuario está autenticado...")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Logout'] | //a[@href='/cart']"))
    )
    print("✅ Usuario autenticado: Logout o carrito visible.")

    print("🔍 [9] Eliminando overlays que puedan interceptar clics...")
    driver.execute_script(
        "document.querySelectorAll('.fixed.inset-0.z-50, .modal, .overlay, "
        "[class*=\"bg-background/70\"]').forEach(el => el.remove());"
    )

    # ✅ Navegar a la categoría 'Electronics'
    print("🔍 [10] Navegando a 'Electronics'...")
    electronics_category_page = home_page.click_electronics_category()
    assert electronics_category_page is not None, "click_electronics_category() devolvió None"
    print("✅ Categoría 'Electronics' abierta.")

    # ✅ Buscar y hacer clic en el producto 21 por su botón "View Details"
    print("🔍 [11] Buscando producto 21 y haciendo clic en 'View Details'...")
    view_details_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "view-details-21"))
    )
    view_details_btn.click()
    print("✅ Clic en 'View Details' del producto 21 realizado.")

    # ✅ Esperar a que la URL sea la del producto 21
    WebDriverWait(driver, 15).until(EC.url_contains("/product/21"))
    print("✅ URL de producto 21 cargada.")

    # ✅ ELIMINAR TODOS LOS OVERLAYS QUE PUEDAN BLOQUEAR O RETARDAR LA CARGA
    driver.execute_script(
        "document.querySelectorAll('div[role=\"status\"], .loading-overlay, .spinner, .modal, .overlay, "
        ".fixed.inset-0').forEach(el => { if (el) el.remove(); });"
    )

    # ✅ Esperar a que el título del producto sea visible (más confiable)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Smartphone')]"))
    )

    # ✅ Esperar a que el texto "$699.99" aparezca en la página
    WebDriverWait(driver, 20).until(
        lambda d: "$699.99" in d.page_source
    )
    print("✅ Contenido del producto renderizado.")

    # ✅ Eliminar overlays justo antes de buscar el botón
    print("🔍 [12] Eliminando overlays residuales...")
    driver.execute_script(
        "document.querySelectorAll('div[role=\"status\"], .loading-overlay, .overlay, "
        ".spinner, .fixed.inset-0.z-50, [class*=\"bg-background/\"]').forEach(el => { if (el) el.remove(); });"
    )

    # ✅ Esperar a que el botón "Add to Cart" esté presente en el DOM (aunque no sea visible aún)
    print("🛒 Esperando que el botón 'Add to Cart' aparezca en el DOM...")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Add to Cart')]"))
    )

    # ✅ Ahora esperar a que sea cliqueable
    print("🛒 Esperando que el botón sea cliqueable...")
    add_to_cart_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add to Cart')]"))
    )
    add_to_cart_btn.click()
    print("✅ Agregado al carrito.")

    # --- REEMPLAZO: Ir al carrito navegando directamente a la URL ---
    print("🛒 Navegando directamente a la URL del carrito...")
    driver.get("https://shophub-commerce.vercel.app/cart")
    print("✅ Navegado a la URL del carrito.")

    # ✅ Verificar que el carrito tiene al menos un ítem
    cart_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item, [class*='cart'], h3 + p.text-lg.font-bold"))
    )
    assert len(cart_items) > 0, "Carrito vacío después de agregar un producto."

    # ✅ Verificar que el producto agregado es el esperado
    product_in_cart = driver.find_element(By.CSS_SELECTOR, "h3.font-semibold").text.strip()
    price_in_cart = driver.find_element(By.CSS_SELECTOR, "p.text-lg.font-bold.text-primary").text.strip()

    expected_title = "Smartphone"
    expected_price = "$699.99"

    assert product_in_cart == expected_title, (f"Producto en carrito: '{product_in_cart}', esperado: '{expected_title}'")
    assert price_in_cart == expected_price, (f"Precio en carrito: '{price_in_cart}', esperado: '{expected_price}'")

    print(f"✅ Carrito verificado: '{product_in_cart}' - {price_in_cart}")
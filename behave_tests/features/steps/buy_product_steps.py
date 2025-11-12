import time
from behave import when, then
from pages.shophub.shophub_home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@when('ingreso el email "{email}" y la contraseña "{password}"')
def step_when_ingreso_credenciales(context, email, password):
    email_field = WebDriverWait(context.driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
    )
    password_field = context.driver.find_element(By.XPATH, "//input[@type='password']")
    email_field.clear()
    email_field.send_keys(email)
    password_field.clear()
    password_field.send_keys(password)


@when('hago clic en "Iniciar sesión"')
def step_when_click_iniciar_sesion(context):
    login_button = WebDriverWait(context.driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    context.driver.execute_script("arguments[0].click();", login_button)

    # Eliminar el overlay del DOM para evitar bloqueos futuros
    context.driver.execute_script("""
        const overlays = document.querySelectorAll('div.fixed.inset-0.z-50');
        overlays.forEach(overlay => overlay.remove());
    """)

@when('vuelvo a la página de inicio')
def step_when_vuelvo_a_inicio(context):
    context.driver.get("https://shophub-commerce.vercel.app/")
    # Esperar a que desaparezca cualquier overlay
    WebDriverWait(context.driver, 5).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )

@when('hago clic en la categoría "{categoria}"')
def step_when_click_categoria(context, categoria):
    locator = (By.XPATH, f"//*[normalize-space()='{categoria}']")
    element = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable(locator)
    )
    element.click()

@when('hago clic en el botón "View Details" del primer producto')
def step_when_click_view_details(context):
    # Buscar por texto visible
    button = WebDriverWait(context.driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='View Details']"))
    )
    # Scroll into view (por si está fuera de la pantalla)
    context.driver.execute_script("arguments[0].scrollIntoView(true);", button)
    # Hacer clic con JS para evitar interceptación
    context.driver.execute_script("arguments[0].click();", button)

@when('hago clic en "Add to Cart"')
def step_when_click_add_to_cart(context):
    button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id^='add-to-cart-main']"))
    )
    context.driver.execute_script("arguments[0].click();", button)

    # Esperar un momento breve para que el modal aparezca
    time.sleep(0.5)

    # Eliminar cualquier overlay que pueda haber surgido (modal de confirmación, etc.)
    context.driver.execute_script("""
        const overlays = document.querySelectorAll('div.fixed.inset-0.z-50');
        overlays.forEach(overlay => overlay.remove());
    """)

@then('veo que el carrito tiene al menos un producto')
def step_then_carrito_no_vacio(context):
    # Navegar directamente a la página del carrito
    context.driver.get("https://shophub-commerce.vercel.app/cart")

    # Esperar a que cargue la página y aparezca al menos un nombre de producto
    try:
        product_names = WebDriverWait(context.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.font-semibold"))
        )
        assert len(product_names) > 0, "No se encontraron productos en el carrito"
    except Exception as e:
        # Imprimir el HTML si falla
        print("HTML de la página del carrito:")
        print(context.driver.page_source[:1000])
        raise AssertionError("El carrito está vacío o no se pudo cargar la página") from e
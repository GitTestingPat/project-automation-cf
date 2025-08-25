import pytest
from pytest_bdd import scenarios, given, when, then
from pages.shophub_home_page import HomePage

# Registrar el archivo .feature asociado con los pasos
scenarios('../login_pytestbdd.feature')


# --- Fixture para almacenar el estado entre pasos del escenario BDD---
@pytest.fixture
def scenario_state():
    return {}


# --- Definición de los pasos ---

@given('que estoy en la página de login de ShopHub')
def given_on_login_page(driver, scenario_state):
    """
    Navegar a la página de inicio y hacer clic en Login.
    Almacena la instancia de LoginPage en el estado del escenario.
    """
    home_page = HomePage(driver)
    home_page.go_to()
    login_page = home_page.click_login()  # click_login() devuelve una instancia de LoginPage

    # Guardar la instancia de LoginPage en el estado del escenario
    # para que otros pasos puedan acceder a ella.
    scenario_state['login_page'] = login_page


@when('ingreso credenciales válidas')
def when_enter_valid_credentials(scenario_state):
    """
    Ingresar email y contraseña válidos por defecto.
    Obtiene la instancia de LoginPage del estado del escenario.
    """
    login_page = scenario_state['login_page']
    # Usar credenciales válidas
    login_page.login("testuser@example.com", "password123")


@then('soy redirigido al dashboard')
def then_redirected_to_dashboard(driver):
    """
    Verificar que el login fue exitoso y ya no estamos en la página de login.
    """
    # Verificar que el título ya no debe contener "Login"
    assert "Login" not in driver.title, (
        f"El login parece haber fallado o la redirección no ocurrió. "
        f"El título actual es: '{driver.title}'."
    )
    print("✅ Login exitoso: El título ya no contiene 'Login'.")

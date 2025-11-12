from pytest_bdd import given, when, then
from pages.shophub.shophub_home_page import HomePage

# --- Definición de los pasos ---

@given('que estoy en la página de login de ShopHub')
def given_on_login_page(driver, scenario_state):
    home_page = HomePage(driver)
    home_page.go_to()
    login_page = home_page.click_login()
    scenario_state['login_page'] = login_page

@when('ingreso credenciales válidas')
def when_enter_valid_credentials(scenario_state):
    login_page = scenario_state['login_page']
    login_page.login("testuser@example.com", "password123")

@then('soy redirigido al dashboard')
def then_redirected_to_dashboard(driver):
    assert "Login" not in driver.title, f"Login fallido. Título: {driver.title}"
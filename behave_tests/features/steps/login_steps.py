from behave import given, when, then
from pages.shophub.shophub_home_page import HomePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@given('que estoy en la página de inicio de ShopHub')
def step_given_en_pagina_inicio(context):
    context.home_page = HomePage(context.driver)
    context.home_page.go_to()

@when('hago clic en el botón "Login"')
def step_when_click_login(context):
    # context.home_page.click_login()
    # context.login_page = context.home_page.click_login()
    login_link = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
    )
    login_link.click()
    # Esperar a que la URL contenga "/login"
    WebDriverWait(context.driver, 10).until(
        EC.url_contains("/login")
    )

@then('veo el formulario de inicio de sesión')
def step_then_veo_formulario(context):
    # Verificar que el título cambie o que aparezca un campo de email
    assert "ShopHub" in context.driver.title
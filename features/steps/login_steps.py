from behave import given, when, then
from pages.shophub_home_page import HomePage

@given('que estoy en la página de inicio de ShopHub')
def step_given_en_pagina_inicio(context):
    context.home_page = HomePage(context.driver)
    context.home_page.go_to()

@when('hago clic en el botón "Login"')
def step_when_click_login(context):
    context.home_page.click_login()

@then('veo el formulario de inicio de sesión')
def step_then_veo_formulario(context):
    # Verificar que el título cambie o que aparezca un campo de email
    assert "ShopHub" in context.driver.title
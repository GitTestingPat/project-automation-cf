
Feature: Iniciar sesión en ShopHub

  Scenario: Usuario hace clic en "Login" y ve el formulario
    Given que estoy en la página de inicio de ShopHub
    When hago clic en el botón "Login"
    Then veo el formulario de inicio de sesión
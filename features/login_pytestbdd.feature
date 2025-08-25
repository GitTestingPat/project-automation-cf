Feature: Iniciar sesión en ShopHub con pytest-bdd

  Scenario: Usuario inicia sesión con credenciales válidas
    Given que estoy en la página de login de ShopHub
    When ingreso credenciales válidas
    Then soy redirigido al dashboard

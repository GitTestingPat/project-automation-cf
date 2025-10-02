
Feature: Registro de nuevo usuario con datos válidos
  Como visitante de ShopHub
  Quiero poder registrarme con credenciales válidas
  Para acceder a mi cuenta y usar la plataforma

  Scenario: Registrar un nuevo usuario con datos válidos
    Given estoy en la página principal de ShopHub
    When hago clic en el enlace "Sign Up"
    And completo el formulario de registro con datos válidos
    And envío el formulario de registro
    Then el registro debe ser exitoso
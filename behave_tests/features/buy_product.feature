Feature: Comprar un producto en ShopHub

  Scenario: Usuario inicia sesión, navega a Electronics y agrega un producto al carrito
    Given que estoy en la página de inicio de ShopHub

    When hago clic en el botón "Login"
    And ingreso el email "user@example.com" y la contraseña "password123"
    And hago clic en "Iniciar sesión"
    And vuelvo a la página de inicio
    And hago clic en la categoría "Electronics"
    And hago clic en el botón "View Details" del primer producto
    And hago clic en "Add to Cart"
    Then veo que el carrito tiene al menos un producto
Feature: : Navegación en la página principal de ShopHub
  Como usuario de ShopHub
  Quiero poder navegar por la página principal y las categorías
  Para explorar los productos disponibles

  Scenario: Verificar carga de la página principal
    Given que el usuario accede a la página principal de ShopHub
    Then el título de la página debe contener "ShopHub"
    And los elementos principales deben estar visibles

  Scenario: Navegar a la categoría Men's Clothes
    Given que el usuario está en la página principal de ShopHub
    When el usuario hace clic en la categoría "Men's Clothes"
    Then se deben mostrar productos de la categoría
    And el contador de productos debe ser mayor a 0

  Scenario: Navegar a la categoría Women's Clothes
    Given que el usuario está en la página principal de ShopHub
    When el usuario hace clic en la categoría "Women's Clothes"
    Then se deben mostrar productos de la categoría "Women's Clothes"
    And la página debe contener productos relevantes

  Scenario: Navegar a la categoría Electronics
    Given que el usuario está en la página principal de ShopHub
    When el usuario hace clic en la categoría "Electronics"
    Then se deben mostrar productos de electrónica
    And el usuario debe poder ver los detalles de los productos
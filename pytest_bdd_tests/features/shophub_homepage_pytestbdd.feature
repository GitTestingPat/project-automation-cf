Feature: Navegación en la página principal de ShopHub con pytest-bdd

  Scenario: Verificar carga de la página principal
    Given estoy en la página principal de ShopHub
    Then el título de la página debe contener "ShopHub"
    And los elementos principales deben estar visibles

  Scenario: Navegar a la categoría Men's Clothes
    Given estoy en la página principal de ShopHub
    When hago clic en la categoría "Men's Clothes"
    Then se deben mostrar productos de la categoría
    And el contador de productos debe ser mayor a 0
Feature: Gestión del carrito de compras en ShopHub
  Como usuario de ShopHub
  Quiero poder agregar productos al carrito y gestionar mi compra
  Para realizar compras de manera efectiva

  Background:
    Given que el usuario está en la página principal de ShopHub

  Scenario: Agregar producto al carrito como usuario autenticado
    Given que el usuario inicia sesión con credenciales válidas
    When el usuario navega a la categoría "Men's Clothes"
    And el usuario selecciona el producto "Denim Jeans"
    And el usuario agrega el producto al carrito
    Then el contador del carrito debe incrementarse
    And el producto "Denim Jeans" debe estar en el carrito

  Scenario: Agregar producto al carrito sin autenticación
    When el usuario navega a la categoría "Electronics"
    And el usuario selecciona el primer producto disponible
    And el usuario agrega el producto al carrito
    Then el producto debe agregarse al carrito correctamente

  Scenario: Verificar carrito vacío
    When el usuario accede al carrito
    And el carrito está inicialmente vacío
    Then debe mostrarse el mensaje "Your Cart is Empty"
    And debe mostrarse la descripción del carrito vacío

  Scenario: Ver contenido del carrito con productos
    Given que el usuario inicia sesión con credenciales válidas
    And el usuario ha agregado un producto al carrito
    When el usuario accede al carrito
    Then el carrito debe mostrar los productos agregados
    And cada producto debe tener información visible

  Scenario Outline: Agregar diferentes productos al carrito
    Given que el usuario inicia sesión con credenciales válidas
    When el usuario navega a la categoría "<categoria>"
    And el usuario selecciona el producto "<producto>"
    And el usuario agrega el producto al carrito
    Then el producto "<producto>" debe estar en el carrito

    Examples:
      | categoria      | producto        |
      | Men's Clothes  | Denim Jeans     |
      | Electronics    | Laptop          |
      | Women's Clothes| Summer Dress    |
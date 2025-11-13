Feature: Búsqueda de productos en ShopHub
  Como usuario de ShopHub
  Quiero poder buscar productos por nombre
  Para encontrar rápidamente lo que necesito

  Scenario: Buscar producto existente
    Given que el usuario está en la página principal de ShopHub
    When el usuario busca el producto "Electronics"
    Then el campo de búsqueda debe contener el texto "Electronics"
    And el sistema debe haber procesado la búsqueda

  Scenario: Campo de búsqueda acepta texto
    Given que el usuario está en la página principal de ShopHub
    When el usuario ingresa texto en el campo de búsqueda
    Then el campo debe reflejar el texto ingresado
    And el campo de búsqueda debe estar funcional

  Scenario: Buscar producto con término específico
    Given que el usuario está en la página principal de ShopHub
    When el usuario busca el término "Phone"
    Then el sistema debe mostrar resultados relacionados con "Phone"

  Scenario Outline: Buscar diferentes productos
    Given que el usuario está en la página principal de ShopHub
    When el usuario busca el producto "<producto>"
    Then el campo de búsqueda debe contener el texto "<producto>"

    Examples: :
      | producto    |
      | Electronics |
      | Phone       |
      | Laptop      |
      | Clothes     |
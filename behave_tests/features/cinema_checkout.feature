Feature: Proceso de checkout y pago en Fake Cinema
  Como usuario de Fake Cinema
  Quiero poder completar el proceso de pago
  Para confirmar mi reserva de boletos

  Background:
    Given el usuario ha completado la selección de asientos y boletos

  Scenario: Visualizar el carrito con productos seleccionados
    When el usuario accede al carrito desde la selección de boletos
    Then debe mostrarse un resumen de la compra
    And debe mostrarse el precio total
    And debe estar disponible el botón "Proceder al pago"

  Scenario: Navegar al checkout desde el carrito
    Given el usuario está en la página del carrito
    When el usuario hace clic en "Proceder al pago"
    Then debe mostrarse el formulario de pago
    And todos los campos del formulario deben estar presentes

  Scenario: Completar formulario de pago con datos válidos
    Given el usuario está en la página de checkout
    When el usuario completa el formulario con datos válidos
      | campo       | valor               |
      | firstName   | Bruce               |
      | lastName    | Wayne               |
      | email       | bruce@wayne.com     |
      | cardName    | Bruce Wayne         |
      | cardNumber  | 4111111111111111    |
      | cvv         | 123                 |
    And el usuario hace clic en "Confirmar pago"
    Then debe completarse la compra exitosamente

  Scenario: Validar formato de email inválido
    Given el usuario está en la página de checkout
    When el usuario ingresa un email con formato inválido "admin@demo"
    And el usuario completa los demás campos correctamente
    And el usuario intenta confirmar el pago
    Then el sistema debe rechazar el email inválido

  Scenario: Validar formato de tarjeta de crédito
    Given el usuario está en la página de checkout
    When el usuario ingresa un número de tarjeta válido "4111111111111111"
    Then el campo debe aceptar el número de tarjeta
    And debe permitir completar el pago

  Scenario: Intentar pagar con campo de email vacío
    Given el usuario está en la página de checkout
    When el usuario deja el campo de email vacío
    And el usuario completa los demás campos correctamente
    And el usuario intenta confirmar el pago
    Then debe mostrarse un error de validación

  Scenario: Intentar pagar con campo de número de tarjeta vacío
    Given el usuario está en la página de checkout
    When el usuario deja el campo de número de tarjeta vacío
    And el usuario completa los demás campos correctamente
    And el usuario intenta confirmar el pago
    Then el sistema debe solicitar el número de tarjeta

  Scenario: Intentar pagar con CVV inválido
    Given el usuario está en la página de checkout
    When el usuario ingresa un CVV de 2 dígitos
    And el usuario completa los demás campos correctamente
    And el usuario intenta confirmar el pago
    Then el sistema debe validar el formato del CVV

  Scenario: Intentar ingresar texto en campos numéricos
    Given el usuario está en la página de checkout
    When el usuario intenta ingresar texto en el campo de número de tarjeta
    Then el campo debe rechazar caracteres no numéricos
    And solo debe aceptar números

  Scenario: Volver al inicio desde el carrito
    Given el usuario está en la página del carrito
    When el usuario hace clic en volver al inicio
    Then debe regresar a la página principal del cine

  Scenario: Recargar página durante el proceso de checkout
    Given el usuario está en la página de checkout
    When el usuario recarga la página
    Then debe permanecer en la página de checkout
    And los datos del formulario deben manejarse correctamente

  Scenario Outline: Validar diferentes formatos de tarjeta
    Given el usuario está en la página de checkout
    When el usuario ingresa el número de tarjeta "<numero_tarjeta>"
    Then el sistema debe <resultado> el número de tarjeta

    Examples:
      | numero_tarjeta   | resultado |
      | 4111111111111111 | aceptar   |
      | 1234567890123456 | aceptar   |
Feature: Selección de asientos en Fake Cinema
  Como usuario de Fake Cinema
  Quiero poder seleccionar y gestionar asientos
  Para reservar los mejores lugares para ver la película

  Background:
    Given que el usuario está en la sala de selección de asientos

  Scenario: Seleccionar un asiento disponible
    When el usuario selecciona el primer asiento disponible
    Then el asiento debe marcarse como seleccionado
    And el botón "Comprar boletos" debe estar habilitado
    And debe mostrarse el precio del asiento

  Scenario: Seleccionar múltiples asientos
    When el usuario selecciona 3 asientos disponibles
    Then los 3 asientos deben estar seleccionados
    And el precio total debe reflejar los 3 asientos
    And el botón "Comprar boletos" debe estar habilitado

  Scenario: Deseleccionar un asiento previamente seleccionado
    Given que el usuario ha seleccionado un asiento
    When el usuario hace clic nuevamente en el mismo asiento
    Then el asiento debe deseleccionarse
    And el precio debe actualizarse

  Scenario: Intentar seleccionar un asiento ocupado
    When el usuario intenta seleccionar un asiento ocupado
    Then el asiento no debe poder seleccionarse
    And debe permanecer marcado como ocupado

  Scenario: Visualizar el estado de los asientos
    Then deben mostrarse asientos disponibles en color azul
    And deben mostrarse asientos ocupados en otro color
    And la sala debe tener una distribución clara de asientos

  Scenario: Seleccionar asientos para accesibilidad
    When el usuario hace clic en el ícono de silla de ruedas
    Then debe poder identificar espacios de accesibilidad
    And el sistema debe mostrar opciones accesibles

  Scenario: Comprar boletos después de seleccionar asiento
    Given que el usuario ha seleccionado un asiento
    When el usuario hace clic en "Comprar boletos"
    Then debe mostrarse el modal de selección de boletos
    And debe poder seleccionar el tipo y cantidad de boletos

  Scenario Outline: Seleccionar diferentes cantidades de asientos
    When el usuario selecciona <cantidad> asientos disponibles
    Then los <cantidad> asientos deben estar seleccionados
    And el botón "Comprar boletos" debe estar habilitado

    Examples:
      | cantidad |
      | 1        |
      | 2        |
      | 3        |
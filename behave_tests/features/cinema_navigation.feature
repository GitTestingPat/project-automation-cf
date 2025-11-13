Feature: Navegación y selección de películas en Fake Cinema
  Como usuario de Fake Cinema
  Quiero poder navegar por la cartelera y seleccionar películas
  Para reservar boletos para ver una película

  Scenario: Verificar acceso a la página principal del cine
    Given que el usuario accede a la página principal de Fake Cinema
    Then el título principal debe ser "¡El mismo héroe, como nunca antes!"
    And los botones de "Ver detalle" deben estar visibles
    And la URL debe contener "fake-cinema.vercel.app"
    And la página no debe mostrar errores

  Scenario: Seleccionar película desde la cartelera
    Given que el usuario está en la página principal de Fake Cinema
    When el usuario hace clic en "Ver detalle" de "Jurassic World"
    Then debe mostrarse la página de detalles de la película
    And debe mostrarse información de horarios disponibles

  Scenario: Navegar a detalles de película Los 4 Fantásticos
    Given que el usuario está en la página principal de Fake Cinema
    When el usuario hace clic en "Ver detalle" de "Fantastic Four"
    Then debe mostrarse la página de detalles de "Fantastic Four"
    And deben estar disponibles las opciones de fecha y hora

  Scenario: Seleccionar fecha y hora para una película
    Given que el usuario está viendo los detalles de una película
    When el usuario selecciona la primera fecha disponible
    And el usuario selecciona la primera hora disponible
    Then debe cargarse la sala de selección de asientos

  Scenario: Visualizar cartelera de películas disponibles
    Given que el usuario accede a la página principal de Fake Cinema
    Then debe mostrarse al menos una película en la cartelera
    And cada película debe tener un botón de "Ver detalle"
    And las imágenes de las películas deben cargarse correctamente

  Scenario: Filtrar películas por cine
    Given que el usuario está viendo los detalles de una película
    When el usuario aplica un filtro de cine
    Then deben actualizarse los horarios disponibles según el cine seleccionado

  Scenario: Verificar clasificación de películas
    Given que el usuario está viendo los detalles de una película
    Then debe mostrarse la clasificación de la película
    And la clasificación debe ser visible para el usuario
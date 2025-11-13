Feature: Navegación y selección de películas en Fake Cinema con pytest-bdd

  Scenario: Verificar acceso a la página principal del cine
    Given estoy en la página principal de Fake Cinema
    Then el título principal debe ser "¡El mismo héroe, como nunca antes!"
    And los botones de "Ver detalle" deben estar visibles
    And la URL debe contener "fake-cinema.vercel.app"

  Scenario: Seleccionar película desde la cartelera
    Given estoy en la página principal de Fake Cinema
    When hago clic en "Ver detalle" de "Jurassic World"
    Then debe mostrarse la página de detalles de la película
    And debe mostrarse información de horarios disponibles

  Scenario: Seleccionar asiento en la sala
    Given estoy en la sala de selección de asientos de Fake Cinema
    When selecciono el primer asiento disponible
    Then el asiento debe marcarse como seleccionado
    And el botón "Comprar boletos" debe estar habilitado
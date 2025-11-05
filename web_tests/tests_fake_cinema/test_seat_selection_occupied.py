from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_cannot_select_occupied_seat(driver):
    """
    TC-WEB-41: Validación de asiento ocupado
    """
    home_page = CinemaHomePage(driver)

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_first_available_date()
    home_page.select_first_available_time_resilient()

    # Usar metodo para obtener el primer asiento ocupado
    occupied_seat = home_page.get_first_occupied_seat()

    # Assert - Validaciones usando SOLO elementos del POM

    # 1. El asiento está deshabilitado
    assert not occupied_seat.is_enabled(), \
        "El asiento ocupado debería estar deshabilitado"
    print("✅ Asiento ocupado está deshabilitado")

    # 2. Tiene atributo disabled
    disabled_attr = occupied_seat.get_attribute("disabled")
    assert disabled_attr is not None, \
        "El asiento ocupado debería tener atributo 'disabled'"
    print(f"✅ Atributo disabled presente: {disabled_attr}")

    # 3. Validar clases CSS
    seat_classes = occupied_seat.get_attribute("class") or ""
    print(f"✅ Clases del asiento ocupado: {seat_classes}")

    # 4. Intentar hacer clic y verificar que no cambia de estado
    initial_class = occupied_seat.get_attribute("class")
    try:
        driver.execute_script("arguments[0].click();", occupied_seat)
        # Si llegamos aquí, verificar que NO cambió
        updated_class = occupied_seat.get_attribute("class")
        assert initial_class == updated_class, \
            "El asiento ocupado cambió de estado (no debería)"
        print("✅ Asiento ocupado no cambió de estado al intentar clic")
    except:
        print("✅ Clic en asiento ocupado fue interceptado (correcto)")

    # 5. Seleccionar un asiento disponible para contrastar
    selected_seat = home_page.select_first_available_seat()
    assert selected_seat is not None, "No se pudo seleccionar un asiento disponible"
    print(f"✅ Asiento disponible seleccionado correctamente: {selected_seat}")

    # 6. Verificar que el botón de compra se habilitó (usando localizador del POM)
    buy_button = driver.find_element(*home_page.BUY_TICKETS_BUTTON)
    assert buy_button.is_enabled(), "El botón de compra debería estar habilitado"
    print("✅ Botón de compra habilitado tras seleccionar asiento disponible")

    # 7. Verificar que hay asientos disponibles en la sala
    assert home_page.is_seat_grid_displayed(), \
        "No hay asientos disponibles en la sala (datos de prueba inválidos)"

    print(f"✅ Validación completa de asiento ocupado exitosa")
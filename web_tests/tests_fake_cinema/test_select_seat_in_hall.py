from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_select_seat_in_hall(driver):
    """
    TC-WEB-18: Selección de Asiento en la Sala (CORREGIDO)
    """
    home_page = CinemaHomePage(driver)

    # Act
    home_page.go_to()
    home_page.navigate_to_movie_detail(home_page.JURASSIC_WORLD_DETAIL_BUTTON)
    home_page.select_first_available_time_resilient()

    # Seleccionar asiento (este método YA valida internamente que funcionó)
    selected_seat = home_page.select_first_available_seat()

    # Assert - VALIDACIONES usando POM

    # 1. El método debe retornar el número del asiento
    assert selected_seat is not None, "No se retornó información del asiento seleccionado"
    assert selected_seat != "", "El asiento seleccionado está vacío"
    assert selected_seat.isdigit(), f"El asiento no es un número válido: {selected_seat}"

    # 2. Verificar selección usando POM is_seat_selected()
    assert home_page.is_seat_selected(), \
        "El método is_seat_selected() indica que no hay asiento seleccionado"

    # 3. Usar POM click_buy_tickets_button() para verificar flujo completo
    home_page.click_buy_tickets_button()

    # 4. Verificar que el modal de tickets apareció usando POM wait_for_ticket_modal()
    home_page.wait_for_ticket_modal()

    # 5. Seleccionar ticket y confirmar usando POM
    home_page.select_adult_ticket(quantity=1)
    home_page.confirm_tickets_selection()

    print(f"✅ Asiento seleccionado: {selected_seat}")
    print(f"✅ Flujo completo: asiento → comprar → modal → ticket → confirmar")
from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_filtered_by_cinema(driver):
    home_page = CinemaHomePage(driver)
    home_page.go_to()

    # Intentar hacer clic en el botón "Elige tu cine"
    home_page.click_choose_cinema_button()

    # Como el botón no hace nada, verificar que no se haya producido ningún cambio observable.
    # Dado que no hay un estado "esperado" positivo, simplemente confirmar que la acción no tuvo efecto.

    # Aserción intencionalmente falsa para que la prueba falle.
    assert False, ("El botón 'Elige tu cine' no tiene funcionalidad, el botón no hace nada, verificado que "
                   "no se produjo ningún cambio observable.")
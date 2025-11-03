from pages.fake_cinema.cinema_home_page import CinemaHomePage


def test_verify_film_classification_labels(driver):
    """
    TC-WEB-29: Verifica que aparezca el texto de la clasificación en cada película.
    Las clasificaciones esperadas son: A, B, B15, C.
    """
    home_page = CinemaHomePage(driver)
    home_page.go_to()

    # Hacer clic en cada etiqueta de clasificación de película
    home_page.click_film_classification_tag(1)
    home_page.click_film_classification_tag(2)
    home_page.click_film_classification_tag(3)
    home_page.click_film_classification_tag(4)
    home_page.click_film_classification_tag(8)
    home_page.click_film_classification_tag(7)
    home_page.click_film_classification_tag(6)
    home_page.click_film_classification_tag(5)
    home_page.click_film_classification_tag(9)
    home_page.click_film_classification_tag(10)

    # Verificar que las clasificaciones aparecen correctamente
    expected_classifications = ["A", "B", "B15", "C"]
    for classification in expected_classifications:
        assert home_page.is_classification_visible(classification), \
            f"La clasificación {classification} no está visible"
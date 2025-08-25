from selenium.webdriver.common.by import By


class CinemaHomePage:
    def __init__(self, driver):
        self.driver = driver

    # Localizador del título principal (el héroe)
    HERO_TITLE = (By.TAG_NAME, "h2")

    def go_to(self):
        self.driver.get("https://fake-cinema.vercel.app/")

    def get_hero_text(self):
        return self.driver.find_element(*self.HERO_TITLE).text
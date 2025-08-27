from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SIGN_IN_BUTTON = (By.XPATH, "/html/body/main/div/div/div[2]/form/button")
    OVERLAY = (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")

    def enter_email(self, email: str):
        """Ingresar el correo electrónico en el campo correspondiente."""
        # 🔹 En local, esperar a que el campo esté presente
        if not os.getenv("CI"):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.EMAIL_INPUT)
            )
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def enter_password(self, password: str):
        """Ingresar la contraseña en el campo correspondiente."""
        # 🔹 En local, esperar a que el campo esté presente
        if not os.getenv("CI"):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PASSWORD_INPUT)
            )
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_sign_in(self):
        """
        Hacer clic en el botón 'Login'.
        Esperar a que el overlay desaparezca.
        """
        # 1. Esperar a que el overlay desaparezca
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.OVERLAY)
            )
            print("✅ Overlay de carga desapareció.")
        except:
            print("ℹ️  No se encontró un overlay o ya había desaparecido.")

        # 2. Intentar hacer clic en el botón de login
        self.driver.find_element(*self.SIGN_IN_BUTTON).click()

    def login(self, email: str, password: str):
        """
        Flujo completo de login: ingresar credenciales y hacer clic en Sign In.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_sign_in()
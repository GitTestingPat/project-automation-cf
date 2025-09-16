from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SignupPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Localizadores para la página de Registro (Signup)
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "email")
    ZIP_CODE_INPUT = (By.ID, "zipCode")
    PASSWORD_INPUT = (By.ID, "password")
    SIGN_UP_BUTTON = (By.XPATH, "/html/body/main/div/div/div[2]/form/button")

    def go_to(self):
        """Navegar a la página de registro de ShopHub."""
        self.driver.get("https://shophub-commerce.vercel.app/signup")

    def enter_first_name(self, first_name: str):
        """Ingresar el primer nombre en el campo correspondiente."""
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)

    def enter_last_name(self, last_name: str):
        """Ingresar el apellido en el campo correspondiente."""
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)

    def enter_email(self, email: str):
        """Ingresar el correo electrónico en el campo correspondiente."""
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def enter_zip_code(self, zip_code: str):
        """Ingresar el código postal en el campo correspondiente."""
        self.driver.find_element(*self.ZIP_CODE_INPUT).send_keys(zip_code)

    def enter_password(self, password: str):
        """Ingresar la contraseña en el campo correspondiente."""
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_sign_up(self):
        """
        Hacer clic en el botón 'Sign Up'.
        Espera a que el spinner de carga desaparezca antes de hacer clic.
        """
        # 1. Definir el localizador del spinner
        SPINNER = (By.CSS_SELECTOR, "svg.lucide-loader-circle.animate-spin")

        # 2. Esperar a que el spinner desaparezca
        # Usar un tiempo de espera de 10 segundos.
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(SPINNER)
            )
            print("✅ Spinner de carga desapareció.")
        except TimeoutException:
            # Si el spinner no desaparece en 10 segundos, es un problema
            print("⚠️  Spinner de carga sigue visible después de 10 segundos. "
                  "Continuando con el clic de todos modos.")

        # 3. Ahora hacer clic en el botón de Sign Up
        self.driver.find_element(*self.SIGN_UP_BUTTON).click()

    def get_error_message(self) -> str:
        """Obtener el mensaje de error, si existe."""
        try:
            error_element = self.driver.find_element(By.CSS_SELECTOR, ".error-message")
            return error_element.text
        except:
            return ""

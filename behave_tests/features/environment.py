import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import uuid

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario"""
    print("✅ before_scenario ejecutado")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Usar webdriver-manager para obtener el driver automáticamente
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.implicitly_wait(10)


def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario"""
    print("✅ after_scenario ejecutado")
    if hasattr(context, 'driver'):
        context.driver.quit()
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import uuid

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario"""
    print("✅ before_scenario ejecutado")
    options = Options()
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(10)

def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario"""
    print("✅ after_scenario ejecutado")
    if hasattr(context, 'driver'):
        context.driver.quit()
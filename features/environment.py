import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import uuid

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario"""
    options = Options()
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(10)

def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario"""
    if hasattr(context, 'driver'):
        context.driver.quit()
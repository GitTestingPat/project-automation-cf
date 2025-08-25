from selenium import webdriver

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario"""
    context.driver = webdriver.Chrome()
    context.driver.implicitly_wait(10)

def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario"""
    if hasattr(context, 'driver'):
        context.driver.quit()
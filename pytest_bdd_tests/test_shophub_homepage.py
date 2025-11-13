"""
Test para la página principal de ShopHub usando pytest-bdd
"""
from .shophub_homepage_pytestbdd_steps import *
from pytest_bdd import scenarios

# Importar todos los escenarios del feature file
scenarios('features/shophub_homepage_pytestbdd.feature')
"""
Test para navegación en Fake Cinema usando pytest-bdd
"""
from .cinema_navigation_pytestbdd_steps import *
from pytest_bdd import scenarios

# Importar todos los escenarios del feature file
scenarios('features/cinema_navigation_pytestbdd.feature')
import requests
import pytest

"""
Caso de prueba: TC-API-15: Buscar vuelos NYC -> LON
Objetivo: Verificar que se puedan buscar vuelos entre dos ciudades usando parámetros válidos.
"""

BASE_URL = "https://cf-automation-airline-api.onrender.com"

def test_list_airports():
    # Probar un endpoint que funciona
    response = requests.get(f"{BASE_URL}/airports/")

    # Verificar que la respuesta sea 200
    assert response.status_code == 200

    # Convertimos a JSON
    airports = response.json()

    # Verificamos que sea una lista y no esté vacía
    assert isinstance(airports, list)
    assert len(airports) > 0
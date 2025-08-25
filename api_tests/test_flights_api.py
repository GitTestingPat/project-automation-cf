import requests
import pytest

BASE_URL = "https://cf-automation-airline-api.onrender.com"

def test_list_airports():
    # Probemos un endpoint que sí funciona
    response = requests.get(f"{BASE_URL}/airports/")

    # Verificamos que la respuesta sea 200
    assert response.status_code == 200

    # Convertimos a JSON
    airports = response.json()

    # Verificamos que sea una lista y no esté vacía
    assert isinstance(airports, list)
    assert len(airports) > 0
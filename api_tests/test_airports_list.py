import requests
import pytest
from jsonschema import validate


BASE_URL = "https://cf-automation-airline-api.onrender.com"

"""
    TC-API-10: Listar todos los aeropuertos.
    Objetivo: Verificar que se puedan listar todos los aeropuertos disponibles.
"""

def test_list_airports():
    response = requests.get(f"{BASE_URL}/airports")

    # Verificar que la respuesta sea exitosa
    assert response.status_code == 200, f"Esperaba 200, obtuvo {response.status_code}"

    airports = response.json()

    # Verificar que la respuesta sea una lista
    assert isinstance(airports, list), f"Se esperaba una lista, se obtuvo {type(airports)}"

    # Verificar que haya al menos un aeropuerto (o ajustar según el estado conocido de la API)
    # assert len(airports) > 0, "La lista de aeropuertos está vacía"

    # Ejemplo de validación básica de un elemento (si la lista no está vacía)
    if airports:
        first_airport = airports[0]
        # Verificar campos básicos esperados
        assert "iata_code" in first_airport, "Falta 'iata_code' en el aeropuerto"
        assert "city" in first_airport, "Falta 'city' en el aeropuerto"
        assert "country" in first_airport, "Falta 'country' en el aeropuerto"
        # Validar que iata_code tenga 3 letras mayúsculas
    print(f"✅ Listados {len(airports)} aeropuertos.")

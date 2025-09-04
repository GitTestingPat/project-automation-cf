import requests
import time
import pytest
from conftest import BASE_URL

"""
Prueba TC-API-32 Medir tiempo de respuesta del endpoint /airports
Objetivo: verificar el tiempo que le toma al endpoint responder a la petición
"""

def test_get_airports_response_time_under_2_seconds():
    """
    Verificar que el endpoint /airports responda en menos de 2 segundos.
    """
    start_time = time.time()

    response = requests.get(f"{BASE_URL}/airports/")

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Verifica que el código de estado sea exitoso
    assert response.status_code == 200, f"Esperaba 200, obtuvo {response.status_code}"

    # Verifica que el tiempo de respuesta sea menor a 2 segundos
    assert elapsed_time < 2.0, f"Tiempo de respuesta fue {elapsed_time:.2f}s, esperado < 2.0s"

    # Imprime el tiempo para verlo en consola
    print(f"\n⏱ Tiempo de respuesta: {elapsed_time:.2f} segundos")
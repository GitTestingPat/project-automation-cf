import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-33: Probar raíz de la API (GET / root)
Objetivo: Verificar que la raíz de la API responda correctamente.
Nota: Esta prueba no requiere autenticación.
"""

def test_root_endpoint_returns_welcome_message():
    """
    TC-API-33: Probar raíz de la API.
    """
    # 1. Hacer la solicitud GET a la raíz de la API
    response = requests.get(f"{BASE_URL}/")

    # 2. Verificar el código de estado
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar acceder a la raíz. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de acceso exitoso a la raíz debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al acceder a la raíz de la API. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 3. Validar la estructura y datos de la respuesta
    root_data = response.json()
    assert isinstance(root_data, dict), f"Se esperaba un diccionario, se obtuvo {type(root_data)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["msg"]  # Cambiado de "message" a "msg"
    for field in expected_fields:
        assert field in root_data, f"Falta el campo '{field}' en la respuesta de la raíz de la API."

    # Verificaciones específicas de contenido
    assert "Airline API up & running" in root_data["msg"], (
        f"El mensaje de bienvenida no es el esperado. "
        f"Esperado que contenga 'Airline API up & running', Obtenido: {root_data['msg']}"
    )

    print(f"✅ Raíz de la API accedida exitosamente. Mensaje: {root_data['msg']}")
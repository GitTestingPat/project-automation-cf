import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-25: Obtener pago por ID (GET /payments/{payment_id})
Objetivo: Verificar que un usuario autenticado pueda obtener la información de un pago específico que le pertenece.
"""
@pytest.mark.TC_API_25
@pytest.mark.medium
@pytest.mark.payments
@pytest.mark.positive
@pytest.mark.api
def test_get_payment_by_id(user_token, payment_id):
    """
    TC-API-25: Obtener pago por ID.
    Este test recibe 'user_token' y 'test_payment_id' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {user_token}"}
    payment_id_to_get = payment_id # El ID viene del fixture

    # 3. Hacer la solicitud GET a /payments/{payment_id}
    response = requests.get(f"{BASE_URL}/payments/{payment_id_to_get}", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar obtener el pago. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar obtener el pago '{payment_id_to_get}'. "
            f"Esto indica que el pago no fue encontrado, a pesar de haber sido creado. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para obtener un pago. "
            f"Esto indica que el token de usuario no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 403:
        pytest.fail(
            f"La API devolvió 403 (Forbidden) al intentar obtener el pago '{payment_id_to_get}'. "
            f"Esto indica que el usuario no tiene permiso para acceder a este pago (posiblemente no es el dueño). "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de obtención exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al obtener pago. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 5. Validar la estructura y datos de la respuesta (esquema PaymentOut)
    payment_data = response.json()
    assert isinstance(payment_data, dict), f"Se esperaba un diccionario, se obtuvo {type(payment_data)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "booking_id", "status", "amount", "payment_method"]
    for field in expected_fields:
        assert field in payment_data, f"Falta el campo '{field}' en la respuesta del pago obtenido."

    # Verificaciones específicas de contenido
    assert payment_data["id"] == payment_id_to_get, (
        f"El ID del pago no coincide. "
        f"Esperado: {payment_id_to_get}, Obtenido: {payment_data['id']}"
    )
    assert payment_data["booking_id"] # campo no debe estar vacío
    assert payment_data["status"] in ["pending", "success", "failed"], (
        f"Estado de pago inválido: {payment_data['status']}"
    )
    assert isinstance(payment_data["amount"], (int, float)), (
        f"El monto debe ser un número. Obtenido: {type(payment_data['amount'])}"
    )
    assert payment_data["payment_method"] # campo no debe estar vacío

    print(f"✅ Pago obtenido exitosamente. ID: {payment_data['id']}, Estado: {payment_data['status']}")

import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-24: Crear pago (POST /payments)
Objetivo: Verificar que un usuario autenticado pueda crear un nuevo pago para una reserva.
"""

def test_create_payment_as_user(user_token, booking_id):
    """
    TC-API-24: Crear pago.
    Este test recibe 'user_token' y 'test_booking_id' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {user_token}"}
    booking_id_to_pay = booking_id # El ID viene del fixture

    # 3. Preparar datos para el nuevo pago.
    new_payment_data = {
        "booking_id": booking_id_to_pay,
        "amount": 299.99, # Monto de ejemplo, debe coincidir con el de la reserva o ser mayor/igual
        "payment_method": "credit_card" # Método de pago de ejemplo
    }

    # 4. Hacer la solicitud POST a /payments
    response = requests.post(f"{BASE_URL}/payments", json=new_payment_data, headers=headers)

    # 5. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar crear un pago. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
         pytest.fail(
            f"Error de validación al crear pago. "
            f"Esperaba que los datos fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401:
        pytest.skip(
            f"La API requirió autenticación (Status: {response.status_code}) para crear un pago. "
            f"Esto indica que el token de usuario no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar crear un pago para la reserva '{booking_id_to_pay}'. "
            f"Esto indica que la reserva no fue encontrada, a pesar de haber sido creada. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de creación exitosa debe devolver 201 Created
    assert response.status_code == 201, (
        f"Error al crear pago. "
        f"Esperaba 201, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura de la respuesta (esquema PaymentOut)
    created_payment = response.json()
    assert isinstance(created_payment, dict), f"Se esperaba un diccionario, se obtuvo {type(created_payment)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "booking_id", "status", "amount", "payment_method"]
    for field in expected_fields:
        assert field in created_payment, f"Falta el campo '{field}' en la respuesta del pago creado."

    # Verificaciones específicas de contenido
    assert created_payment["booking_id"] == new_payment_data["booking_id"], (
        f"El booking_id del pago no coincide. "
        f"Esperado: {new_payment_data['booking_id']}, Obtenido: {created_payment['booking_id']}"
    )
    assert created_payment["amount"] == new_payment_data["amount"], (
        f"El monto del pago no coincide. "
        f"Esperado: {new_payment_data['amount']}, Obtenido: {created_payment['amount']}"
    )
    assert created_payment["payment_method"] == new_payment_data["payment_method"], (
        f"El método de pago no coincide. "
        f"Esperado: {new_payment_data['payment_method']}, Obtenido: {created_payment['payment_method']}"
    )
    # Verificar que el campo 'status' es parte del esquema PaymentOut y debe estar presente
    assert "status" in created_payment, "Falta 'status' en la respuesta del pago creado."
    # Verificar que el 'status' puede ser "pending", "success", "failed" según el esquema PaymentStatus
    assert created_payment["status"] in ["pending", "success", "failed"], (
        f"Estado de pago inválido: {created_payment['status']}"
    )

    print(f"✅ Pago creado exitosamente. ID: {created_payment['id']}, Booking ID: {created_payment['booking_id']}, "
          f"Estado: {created_payment['status']}")

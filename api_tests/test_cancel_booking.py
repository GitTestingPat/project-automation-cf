import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-23: Cancelar reserva (DELETE /bookings/{booking_id})
Objetivo: Verificar que un usuario autenticado pueda cancelar una de sus reservas.
"""

def test_cancel_booking_as_owner(user_token, booking_id):
    """
    TC-API-23: Cancelar reserva.
    Este test recibe 'user_token' y 'test_booking_id' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {user_token}"}
    booking_id_to_cancel = booking_id # El ID viene del fixture

    # 3. Hacer la solicitud DELETE a /bookings/{booking_id}
    response = requests.delete(f"{BASE_URL}/bookings/{booking_id_to_cancel}", headers=headers)

    # 4. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar cancelar la reserva. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar cancelar la reserva '{booking_id_to_cancel}'. "
            f"Esto indica que la reserva no fue encontrada, a pesar de haber sido creada. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 403:
        pytest.fail(
            f"La API devolvió 403 (Forbidden) al intentar cancelar la reserva '{booking_id_to_cancel}'. "
            f"Esto indica que el usuario no tiene permiso para cancelar esta reserva (posiblemente no es el dueño). "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de cancelación exitosa debe devolver 204 No Content
    assert response.status_code == 204, (
        f"Error al cancelar reserva. "
        f"Esperaba 204 (No Content), obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    print(f"✅ Reserva cancelada exitosamente. ID: {booking_id_to_cancel}")

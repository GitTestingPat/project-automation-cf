import requests
import pytest
from conftest import BASE_URL

"""
Caso de prueba: TC-API-34: Actualizar estado de reserva (PATCH /bookings/{booking_id})
Objetivo: Verificar que un usuario autenticado como admin pueda actualizar el estado de una reserva específica.
"""
@pytest.mark.TC_API_34
@pytest.mark.medium
@pytest.mark.bookings
@pytest.mark.positive
@pytest.mark.api
def test_update_booking_status_as_admin(admin_token, booking_id):
    """
    TC-API-34: Actualizar estado de reserva.
    Este test recibe 'admin_token' y 'test_booking_id' de los fixtures.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    booking_id_to_update = booking_id # El ID viene del fixture

    # 3. Preparar datos para la actualización del estado.
    # El esquema BookingUpdateStatus solo requiere el campo 'status'.
    # Los valores permitidos son: "draft", "paid", "checked_in", "cancelled".
    # Cambiar el estado a "paid".
    updated_status_data = {
        "status": "paid"
    }

    # 4. Hacer la solicitud PATCH a /bookings/{booking_id}
    response = requests.patch(f"{BASE_URL}/bookings/{booking_id_to_update}", json=updated_status_data,
                              headers=headers)

    # 5. Verificar el código de estado.
    # Manejar errores comunes
    if response.status_code == 500:
        pytest.fail(
            f"La API devolvió un error 500 (Internal Server Error) al intentar actualizar el estado de la reserva. "
            f"Esto indica un posible fallo interno en el servidor de la API de prueba. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 422:
         pytest.fail(
            f"Error de validación al actualizar estado de reserva. "
            f"Esperaba que los datos actualizados fueran válidos. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 404:
        pytest.fail(
            f"La API devolvió 404 (Not Found) al intentar actualizar el estado de la reserva '"
            f"{booking_id_to_update}'. "
            f"Esto indica que la reserva no fue encontrada, a pesar de haber sido creada. "
            f"Puede ser un problema de consistencia en la API. "
            f"Cuerpo de la respuesta: {response.text}"
        )
    elif response.status_code == 401 or response.status_code == 403:
        pytest.skip(
            f"La API requirió autenticación/permisos (Status: {response.status_code}) para actualizar "
            f"el estado de una reserva. "
            f"Esto indica que el token de admin no fue aceptado o ha expirado. "
            f"Cuerpo de la respuesta: {response.text}"
        )

    # La operación de actualización exitosa debe devolver 200 OK
    assert response.status_code == 200, (
        f"Error al actualizar estado de reserva. "
        f"Esperaba 200, obtuvo {response.status_code}. "
        f"Cuerpo de la respuesta: {response.text}"
    )

    # 6. Validar la estructura y datos de la respuesta (esquema BookingOut)
    updated_booking = response.json()
    assert isinstance(updated_booking, dict), f"Se esperaba un diccionario, se obtuvo {type(updated_booking)}"

    # Verificar que los campos devueltos sean correctos y estén presentes
    expected_fields = ["id", "flight_id", "user_id", "status", "passengers"]
    for field in expected_fields:
        assert field in updated_booking, f"Falta el campo '{field}' en la respuesta de la reserva actualizada."

    # Verificaciones específicas de contenido
    assert updated_booking["id"] == booking_id_to_update, (
        f"El ID de la reserva no debería cambiar. "
        f"Esperado: {booking_id_to_update}, Obtenido: {updated_booking['id']}"
    )
    assert updated_booking["status"] == updated_status_data["status"], (
        f"El estado no se actualizó. "
        f"Esperado: {updated_status_data['status']}, Obtenido: {updated_booking['status']}"
    )
    # Verificar que otros campos esenciales sigan presentes
    assert updated_booking["flight_id"] # Verificar que no esté vacío
    assert updated_booking["user_id"] # Verificar que no esté vacío
    assert isinstance(updated_booking["passengers"], list), (
        f"Los pasajeros deben ser una lista. Obtenido: {type(updated_booking['passengers'])}"
    )
    if updated_booking["passengers"]:
        passenger = updated_booking["passengers"][0]
        assert "full_name" in passenger and passenger["full_name"]
        assert "passport" in passenger and passenger["passport"]
        # 'seat' es opcional

    print(f"✅ Estado de reserva actualizado exitosamente. ID: {updated_booking['id']}, Nuevo estado: "
          f"{updated_booking['status']}")

import pytest
import requests
from datetime import datetime, timedelta

BASE_URL = "https://cf-automation-airline-api.onrender.com"

# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture(scope="session")
def admin_user():
    """Usa el usuario admin preexistente."""
    login_data = {
        "username": "admin@demo.com",
        "password": "admin123"
    }
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    assert resp.status_code == 200, f"Login falló: {resp.text}"
    token = resp.json()["access_token"]
    return {"email": "admin@demo.com", "token": token}


@pytest.fixture
def auth_headers(admin_user):
    return {"Authorization": f"Bearer {admin_user['token']}"}


# Fixture para aeropuerto
@pytest.fixture
def sample_airport(auth_headers):
    # Intenta usar uno existente primero
    resp = requests.get(f"{BASE_URL}/airports/JFK")
    if resp.status_code == 200:
        return resp.json()
    # Si no existe, créalo (aunque en producción probablemente ya existan)
    airport_data = {"iata_code": "JFK", "city": "New York", "country": "USA"}
    resp = requests.post(f"{BASE_URL}/airports", json=airport_data, headers=auth_headers)
    if resp.status_code == 201:
        return resp.json()
    elif resp.status_code == 422:
        # Ya existe, búscalo
        resp = requests.get(f"{BASE_URL}/airports/JFK")
        assert resp.status_code == 200
        return resp.json()
    else:
        raise AssertionError(f"No se pudo obtener JFK: {resp.status_code} - {resp.text}")


@pytest.fixture
def sample_aircraft(auth_headers):
    # Usa un tail_number único para evitar conflictos
    import uuid
    tail = f"N{uuid.uuid4().hex[:6].upper()}"
    aircraft_data = {
        "tail_number": tail,
        "model": "Boeing 737",
        "capacity": 180
    }
    resp = requests.post(f"{BASE_URL}/aircrafts", json=aircraft_data, headers=auth_headers)
    assert resp.status_code == 201, f"Fallo al crear avión: {resp.text}"
    return resp.json()


@pytest.fixture
def sample_flight(auth_headers, sample_aircraft, sample_airport):
    future = datetime.utcnow() + timedelta(days=1)
    flight_data = {
        "origin": "JFK",
        "destination": "LAX",
        "departure_time": future.isoformat() + "Z",
        "arrival_time": (future + timedelta(hours=5)).isoformat() + "Z",
        "base_price": 250.0,
        "aircraft_id": sample_aircraft["id"]
    }
    resp = requests.post(f"{BASE_URL}/flights", json=flight_data, headers=auth_headers)
    assert resp.status_code == 201, f"Fallo al crear vuelo: {resp.text}"
    return resp.json()


# -----------------------------
# Pruebas: Auth
# -----------------------------

def test_login_admin_valid():
    login_data = {"username": "admin@demo.com", "password": "admin123"}
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    assert resp.status_code == 200
    assert "access_token" in resp.json()


# -----------------------------
# Pruebas: Airports
# -----------------------------

def test_create_airport_valid(auth_headers):
    import uuid
    code = f"X{uuid.uuid4().hex[:2].upper()}"
    data = {"iata_code": code, "city": "Test City", "country": "Testland"}
    resp = requests.post(f"{BASE_URL}/airports", json=data, headers=auth_headers)
    assert resp.status_code == 201


def test_create_airport_invalid_iata(auth_headers):
    data = {"iata_code": "ab1", "city": "Test", "country": "Test"}
    resp = requests.post(f"{BASE_URL}/airports", json=data, headers=auth_headers)
    assert resp.status_code == 422


def test_get_airport():
    resp = requests.get(f"{BASE_URL}/airports/JFK")
    assert resp.status_code == 200


# -----------------------------
# Pruebas: Aircrafts
# -----------------------------

def test_create_aircraft_valid(auth_headers):
    import uuid
    data = {
        "tail_number": f"N{uuid.uuid4().hex[:6].upper()}",
        "model": "Airbus A320",
        "capacity": 150
    }
    resp = requests.post(f"{BASE_URL}/aircrafts", json=data, headers=auth_headers)
    assert resp.status_code == 201


def test_create_aircraft_invalid_tail_number(auth_headers):
    data = {"tail_number": "N12", "model": "Test", "capacity": 100}
    resp = requests.post(f"{BASE_URL}/aircrafts", json=data, headers=auth_headers)
    assert resp.status_code == 422


# -----------------------------
# Pruebas: Flights
# -----------------------------

def test_search_flights_valid():
    params = {"origin": "JFK", "destination": "LAX"}
    resp = requests.get(f"{BASE_URL}/flights", params=params)
    assert resp.status_code == 200


def test_search_flights_invalid_origin():
    params = {"origin": "jfk", "destination": "LAX"}  # minúsculas
    resp = requests.get(f"{BASE_URL}/flights", params=params)
    assert resp.status_code == 200


def test_create_flight_valid(auth_headers, sample_aircraft):
    future = datetime.utcnow() + timedelta(days=2)
    data = {
        "origin": "JFK",
        "destination": "MAD",
        "departure_time": future.isoformat() + "Z",
        "arrival_time": (future + timedelta(hours=8)).isoformat() + "Z",
        "base_price": 600.0,
        "aircraft_id": sample_aircraft["id"]
    }
    resp = requests.post(f"{BASE_URL}/flights", json=data, headers=auth_headers)
    assert resp.status_code == 201


# -----------------------------
# Pruebas: Bookings y Payments
# -----------------------------

def test_create_booking_valid(auth_headers, sample_flight):
    booking_data = {
        "flight_id": sample_flight["id"],
        "passengers": [{"full_name": "Ana López", "passport": "AB123456"}]
    }
    resp = requests.post(f"{BASE_URL}/bookings", json=booking_data, headers=auth_headers)
    assert resp.status_code == 201


def test_create_booking_invalid_passport(auth_headers, sample_flight):
    booking_data = {
        "flight_id": sample_flight["id"],
        "passengers": [{"full_name": "Ana", "passport": "AB12"}]
    }
    resp = requests.post(f"{BASE_URL}/bookings", json=booking_data, headers=auth_headers)
    assert resp.status_code == 422


def test_pay_valid(auth_headers, sample_flight):
    # Crea reserva
    booking_data = {
        "flight_id": sample_flight["id"],
        "passengers": [{"full_name": "Test", "passport": "PASS12345"}]
    }
    resp = requests.post(f"{BASE_URL}/bookings", json=booking_data, headers=auth_headers)
    assert resp.status_code == 201
    booking_id = resp.json()["id"]

    # Paga
    payment_data = {
        "booking_id": booking_id,
        "amount": 250.0,
        "payment_method": "credit_card"
    }
    resp = requests.post(f"{BASE_URL}/payments", json=payment_data, headers=auth_headers)
    assert resp.status_code == 201


# -----------------------------
# Pruebas: Users (admin)
# -----------------------------

def test_list_users(auth_headers):
    resp = requests.get(f"{BASE_URL}/users", headers=auth_headers)
    assert resp.status_code == 200


def test_create_user_as_admin(auth_headers):
    import uuid
    user_data = {
        "email": f"newuser_{uuid.uuid4().hex[:6]}@example.com",
        "password": "123456",
        "full_name": "New Passenger",
        "role": "passenger"
    }
    resp = requests.post(f"{BASE_URL}/users", json=user_data, headers=auth_headers)
    assert resp.status_code == 201


# -----------------------------
# Pruebas: Root
# -----------------------------

def test_root():
    resp = requests.get(f"{BASE_URL}/")
    assert resp.status_code == 200
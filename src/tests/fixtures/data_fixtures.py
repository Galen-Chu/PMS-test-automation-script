"""
Test data fixtures for pytest tests.
Provides reusable test data across all test files.
"""

import json
import csv
from datetime import date
from pathlib import Path
from typing import Dict, List, Any
import pytest
from faker import Faker

# Initialize Faker for random data generation
fake = Faker()

# Data directory path
DATA_DIR = Path(__file__).parent / "data"


def load_json_data(file_path: str) -> Dict[str, Any]:
    """Load JSON data from file."""
    full_path = DATA_DIR / file_path
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_data(file_path: str) -> List[Dict[str, str]]:
    """Load CSV data from file."""
    full_path = DATA_DIR / file_path
    with open(full_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ============================================================================
# Guest Data Fixtures
# ============================================================================


@pytest.fixture
def guest_data() -> Dict[str, Any]:
    """Load all guest test data."""
    return load_json_data("guests/guest_data.json")


@pytest.fixture
def valid_guest(guest_data) -> Dict[str, str]:
    """Get valid guest data for testing."""
    return guest_data["valid_guest"]


@pytest.fixture
def vip_guest(guest_data) -> Dict[str, str]:
    """Get VIP guest data for testing."""
    return guest_data["vip_guest"]


@pytest.fixture
def corporate_guest(guest_data) -> Dict[str, str]:
    """Get corporate guest data for testing."""
    return guest_data["corporate_guest"]


@pytest.fixture
def international_guest(guest_data) -> Dict[str, str]:
    """Get international guest data for testing."""
    return guest_data["international_guest"]


@pytest.fixture
def invalid_guest_missing_email(guest_data) -> Dict[str, str]:
    """Get invalid guest data (missing email)."""
    return guest_data["invalid_guest_missing_email"]


@pytest.fixture
def invalid_guest_invalid_email(guest_data) -> Dict[str, str]:
    """Get invalid guest data (invalid email format)."""
    return guest_data["invalid_guest_invalid_email"]


@pytest.fixture
def invalid_guest_missing_name(guest_data) -> Dict[str, str]:
    """Get invalid guest data (missing name)."""
    return guest_data["invalid_guest_missing_name"]


@pytest.fixture
def random_guest() -> Dict[str, str]:
    """Generate random guest data using Faker."""
    return {
        "name": fake.name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.street_address(),
        "city": fake.city(),
        "country": fake.country(),
        "postal_code": fake.postcode(),
        "company": fake.company(),
        "job": fake.job(),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
    }


@pytest.fixture
def bulk_guests() -> List[Dict[str, str]]:
    """Load bulk guest data from CSV."""
    return load_csv_data("guests/bulk_guests.csv")


# ============================================================================
# Reservation Data Fixtures
# ============================================================================


@pytest.fixture
def reservation_data() -> Dict[str, Any]:
    """Load all reservation test data."""
    return load_json_data("reservations/reservation_data.json")


@pytest.fixture
def valid_reservation(reservation_data) -> Dict[str, Any]:
    """Get valid reservation data for testing."""
    return reservation_data["valid_reservation"]


@pytest.fixture
def weekend_reservation(reservation_data) -> Dict[str, Any]:
    """Get weekend reservation data."""
    return reservation_data["weekend_reservation"]


@pytest.fixture
def group_reservation(reservation_data) -> Dict[str, Any]:
    """Get group reservation data."""
    return reservation_data["group_reservation"]


@pytest.fixture
def long_stay_reservation(reservation_data) -> Dict[str, Any]:
    """Get long stay reservation data."""
    return reservation_data["long_stay_reservation"]


@pytest.fixture
def corporate_reservation(reservation_data) -> Dict[str, Any]:
    """Get corporate reservation data."""
    return reservation_data["corporate_reservation"]


@pytest.fixture
def invalid_reservation_past_date(reservation_data) -> Dict[str, Any]:
    """Get invalid reservation data (past date)."""
    return reservation_data["invalid_reservation_past_date"]


@pytest.fixture
def invalid_reservation_date_order(reservation_data) -> Dict[str, Any]:
    """Get invalid reservation data (departure before arrival)."""
    return reservation_data["invalid_reservation_departure_before_arrival"]


@pytest.fixture
def random_reservation() -> Dict[str, Any]:
    """Generate random reservation data."""
    arrival_date = fake.date_between(start_date="today", end_date="+30d")
    departure_date = fake.date_between(start_date=arrival_date, end_date="+60d")

    return {
        "guest_name": fake.name(),
        "arrival_date": arrival_date.isoformat(),
        "departure_date": departure_date.isoformat(),
        "room_type": fake.random_element(["STANDARD", "DELUXE", "SUITE", "FAMILY"]),
        "adults": fake.random_int(min=1, max=4),
        "children": fake.random_int(min=0, max=3),
        "rate_amount": round(fake.pyfloat(min_value=99, max_value=299), 2),
        "currency": "USD",
        "email": fake.email(),
        "phone": fake.phone_number(),
        "special_requests": fake.sentence(),
    }


# ============================================================================
# Room Data Fixtures
# ============================================================================


@pytest.fixture
def room_data() -> Dict[str, Any]:
    """Load all room test data."""
    return load_json_data("rooms/room_data.json")


@pytest.fixture
def room_types(room_data) -> List[Dict[str, Any]]:
    """Get list of room types."""
    return room_data["room_types"]


@pytest.fixture
def room_statuses(room_data) -> List[Dict[str, Any]]:
    """Get list of room statuses."""
    return room_data["room_statuses"]


@pytest.fixture
def sample_rooms(room_data) -> List[Dict[str, Any]]:
    """Get list of sample rooms."""
    return room_data["sample_rooms"]


@pytest.fixture
def random_room(room_types) -> Dict[str, Any]:
    """Get random room type."""
    return fake.random_element(room_types)


# ============================================================================
# Configuration Fixtures
# ============================================================================


@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Load test configuration."""
    return load_json_data("settings/test_config.json")


@pytest.fixture
def browser_settings(test_config) -> Dict[str, Any]:
    """Get browser settings."""
    return test_config["browser_settings"]


@pytest.fixture
def timeout_settings(test_config) -> Dict[str, int]:
    """Get timeout settings."""
    return test_config["timeout_settings"]


# ============================================================================
# Data Generator Fixtures
# ============================================================================


@pytest.fixture
def guest_factory():
    """Factory for creating guest data."""

    def _create_guest(
        name: str = None, email: str = None, phone: str = None, **kwargs
    ) -> Dict[str, str]:
        return {
            "name": name or fake.name(),
            "email": email or fake.email(),
            "phone": phone or fake.phone_number(),
            "address": kwargs.get("address", fake.street_address()),
            "city": kwargs.get("city", fake.city()),
            "country": kwargs.get("country", fake.country()),
            **kwargs,
        }

    return _create_guest


@pytest.fixture
def reservation_factory():
    """Factory for creating reservation data."""

    def _create_reservation(
        guest_name: str = None,
        arrival_date: str = None,
        departure_date: str = None,
        room_type: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        arrival = arrival_date or fake.date_between(start_date="today", end_date="+30d").isoformat()
        departure = (
            departure_date
            or fake.date_between(
                # faker no longer parses ISO date strings - pass a date object
                start_date=date.fromisoformat(arrival),
                end_date="+60d",
            ).isoformat()
        )

        return {
            "guest_name": guest_name or fake.name(),
            "arrival_date": arrival,
            "departure_date": departure,
            "room_type": room_type or fake.random_element(["STANDARD", "DELUXE", "SUITE"]),
            "adults": kwargs.get("adults", fake.random_int(min=1, max=4)),
            "children": kwargs.get("children", fake.random_int(min=0, max=2)),
            "email": kwargs.get("email", fake.email()),
            "phone": kwargs.get("phone", fake.phone_number()),
            **kwargs,
        }

    return _create_reservation


# ============================================================================
# Cleanup Fixtures
# ============================================================================


@pytest.fixture
def cleanup_tracker():
    """Track resources created during tests for cleanup."""
    created_resources = {"guests": [], "reservations": [], "rooms": []}

    yield created_resources

    # Cleanup is handled by the test using this fixture
    # This is just a tracking mechanism


# ============================================================================
# Parametrized Fixtures
# ============================================================================


@pytest.fixture(params=["valid_guest", "vip_guest", "corporate_guest", "international_guest"])
def various_guest_types(request, guest_data):
    """Parametrized fixture for different guest types."""
    return guest_data[request.param]


@pytest.fixture(params=["STANDARD", "DELUXE", "SUITE", "FAMILY"])
def various_room_types(request):
    """Parametrized fixture for different room types."""
    return request.param


# ============================================================================
# Helper Functions
# ============================================================================


def merge_dicts(base: Dict, override: Dict) -> Dict:
    """Merge two dictionaries with override taking precedence."""
    return {**base, **override}


def generate_bulk_guests(count: int) -> List[Dict[str, str]]:
    """Generate multiple random guests."""
    return [random_guest() for _ in range(count)]


def date_range(start_date: str, end_date: str) -> List[str]:
    """Generate list of dates between start and end."""
    from datetime import datetime, timedelta

    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    dates = []
    current = start
    while current <= end:
        dates.append(current.isoformat())
        current += timedelta(days=1)

    return dates

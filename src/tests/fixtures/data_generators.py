"""
Programmatic test data generators.

Faker-based factories for guests, reservations, rooms and payments,
plus a builder (``create_test_scenario``) for complete booking
scenarios. Complements the pytest fixtures in ``data_fixtures.py``,
which load static JSON/CSV data.
"""

import itertools
import uuid
from datetime import date, timedelta

from faker import Faker

fake = Faker()
_unique_counter = itertools.count(1)


def generate_unique_id(prefix: str = "id") -> str:
    """Return a human-friendly unique id, e.g. ``guest-000123-a1b2``."""
    return f"{prefix}-{next(_unique_counter):06d}-{uuid.uuid4().hex[:4]}"


class GuestDataGenerator:
    """Generate guest dictionaries."""

    FIELDS = ("name", "email", "phone", "id_number", "vip_status", "notes")

    @classmethod
    def create_guest(cls, **overrides) -> dict:
        guest = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "id_number": fake.numerify(text="A#######"),
            "vip_status": "normal",
            "notes": "",
        }
        guest.update(overrides)
        return guest

    @classmethod
    def create_bulk_guests(cls, count: int) -> list:
        return [cls.create_guest() for _ in range(count)]


class ReservationDataGenerator:
    """Generate reservation dictionaries with consistent date logic."""

    @classmethod
    def create_reservation(cls, **overrides) -> dict:
        arrival = date.today() + timedelta(days=fake.random_int(min=1, max=30))
        nights = fake.random_int(min=1, max=7)
        reservation = {
            "reservation_no": generate_unique_id("RES"),
            "guest_name": fake.name(),
            "room_type": fake.random_element(elements=("STD", "DLX", "SUITE")),
            "adults": fake.random_int(min=1, max=4),
            "arrival_date": arrival.isoformat(),
            "departure_date": (arrival + timedelta(days=nights)).isoformat(),
        }
        reservation.update(overrides)
        return reservation

    @classmethod
    def create_bulk_reservations(cls, count: int) -> list:
        return [cls.create_reservation() for _ in range(count)]


class RoomDataGenerator:
    """Generate room dictionaries."""

    @classmethod
    def create_room(cls, **overrides) -> dict:
        room = {
            "room_no": fake.numerify(text="###"),
            "room_type": fake.random_element(elements=("STD", "DLX", "SUITE")),
            "floor": fake.random_int(min=1, max=12),
            "status": fake.random_element(elements=("VA", "OC", "DD")),
        }
        room.update(overrides)
        return room


class PaymentDataGenerator:
    """Generate payment dictionaries."""

    @classmethod
    def create_payment(cls, **overrides) -> dict:
        payment = {
            "payment_no": generate_unique_id("PAY"),
            "method": fake.random_element(elements=("CASH", "CARD", "TRANSFER")),
            "amount": round(fake.random_int(min=1000, max=99999) / 100.0, 2),
            "paid_at": fake.date_time_this_year().isoformat(),
        }
        payment.update(overrides)
        return payment


class TestDataBuilder:
    """Builder for complete booking scenarios.

    ``create_test_scenario()`` returns a fresh builder; chain the
    ``with_*`` methods and call ``build()`` for the scenario dict.
    """

    def __init__(self):
        self._guest = None
        self._reservation = None
        self._room = None
        self._payments = []

    def with_guest(self, **overrides):
        self._guest = GuestDataGenerator.create_guest(**overrides)
        return self

    def with_vip_guest(self, **overrides):
        overrides.setdefault("vip_status", "platinum")
        return self.with_guest(**overrides)

    def with_reservation(self, **overrides):
        if self._guest and "guest_name" not in overrides:
            overrides["guest_name"] = self._guest["name"]
        self._reservation = ReservationDataGenerator.create_reservation(**overrides)
        return self

    def with_room(self, **overrides):
        self._room = RoomDataGenerator.create_room(**overrides)
        return self

    def with_payment(self, amount, **overrides):
        self._payments.append(PaymentDataGenerator.create_payment(amount=amount, **overrides))
        return self

    def build(self) -> dict:
        return {
            "guest": self._guest or GuestDataGenerator.create_guest(),
            "reservation": self._reservation or ReservationDataGenerator.create_reservation(),
            "room": self._room or RoomDataGenerator.create_room(),
            "payments": list(self._payments),
        }


def create_test_scenario() -> TestDataBuilder:
    """Entry point of the builder chain: ``create_test_scenario().with_...().build()``."""
    return TestDataBuilder()

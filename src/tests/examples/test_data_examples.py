"""
Example tests demonstrating test data usage.

This file shows how to use:
- Static test data from JSON/CSV files
- Dynamic test data generation with Faker
- Parametrized tests with multiple data sets
- Data factories for flexible test data creation
"""

import pytest

pytestmark = [pytest.mark.smoke]
from tests.fixtures import GuestDataGenerator, ReservationDataGenerator, create_test_scenario


class TestGuestCreation:
    """Examples of testing guest creation with various data sources."""

    def test_create_guest_with_static_data(self, valid_guest):
        """Test using static data from JSON file."""
        # valid_guest comes from fixtures/data_fixtures.py
        assert valid_guest["email"] is not None
        assert "@" in valid_guest["email"]
        assert valid_guest["name"] == "John Doe"

    def test_create_guest_with_random_data(self, random_guest):
        """Test using randomly generated data."""
        # random_guest is generated fresh each time using Faker
        assert random_guest["email"] is not None
        assert random_guest["phone"] is not None
        print(f"Testing with random guest: {random_guest['name']}")

    def test_create_vip_guest(self, vip_guest):
        """Test VIP guest creation."""
        assert vip_guest["vip_status"] == "platinum"
        assert vip_guest["loyalty_number"] is not None

    @pytest.mark.parametrize(
        "guest_type", ["valid_guest", "vip_guest", "corporate_guest", "international_guest"]
    )
    def test_create_various_guest_types(self, guest_type, guest_data):
        """Parametrized test with multiple guest types."""
        guest = guest_data[guest_type]
        assert guest["name"] is not None
        assert guest["email"] is not None

    def test_create_custom_guest_with_factory(self, guest_factory):
        """Test using factory to create custom guest."""
        # Use factory to create guest with specific attributes
        custom_guest = guest_factory(
            name="Custom User", email="custom@example.com", country="Canada"
        )

        assert custom_guest["name"] == "Custom User"
        assert custom_guest["email"] == "custom@example.com"
        assert custom_guest["country"] == "Canada"

    def test_invalid_guest_missing_email(self, invalid_guest_missing_email):
        """Test validation with invalid data."""
        # This should fail validation (no email)
        assert (
            "email" not in invalid_guest_missing_email
            or invalid_guest_missing_email.get("email") is None
        )


class TestReservationCreation:
    """Examples of testing reservation creation."""

    def test_create_reservation_with_static_data(self, valid_reservation):
        """Test using static reservation data."""
        assert valid_reservation["guest_name"] == "John Doe"
        assert valid_reservation["room_type"] == "DELUXE"
        assert valid_reservation["adults"] >= 1

    def test_create_reservation_with_random_data(self, random_reservation):
        """Test using randomly generated reservation."""
        assert random_reservation["arrival_date"] is not None
        assert random_reservation["departure_date"] is not None

        # Verify departure is after arrival
        from datetime import datetime

        arrival = datetime.fromisoformat(random_reservation["arrival_date"])
        departure = datetime.fromisoformat(random_reservation["departure_date"])
        assert departure > arrival

    def test_create_weekend_reservation(self, weekend_reservation):
        """Test weekend-specific reservation."""
        from datetime import datetime

        arrival = datetime.fromisoformat(weekend_reservation["arrival_date"])
        departure = datetime.fromisoformat(weekend_reservation["departure_date"])

        # Verify it's a weekend stay
        assert arrival.weekday() == 4  # Friday
        assert departure.weekday() == 6  # Sunday

    def test_create_reservation_with_factory(self, reservation_factory):
        """Test using factory to create custom reservation."""
        custom_reservation = reservation_factory(
            guest_name="Factory Guest", room_type="SUITE", adults=2, children=1
        )

        assert custom_reservation["guest_name"] == "Factory Guest"
        assert custom_reservation["room_type"] == "SUITE"
        assert custom_reservation["adults"] == 2
        assert custom_reservation["children"] == 1

    def test_invalid_reservation_dates(self, invalid_reservation_date_order):
        """Test validation catches invalid date order."""
        from datetime import datetime

        arrival = datetime.fromisoformat(invalid_reservation_date_order["arrival_date"])
        departure = datetime.fromisoformat(invalid_reservation_date_order["departure_date"])

        # This should fail validation (departure before arrival)
        assert departure < arrival


class TestBulkData:
    """Examples of testing with bulk data."""

    def test_bulk_guests_from_csv(self, bulk_guests):
        """Test loading bulk guest data from CSV."""
        assert len(bulk_guests) == 10

        for guest in bulk_guests:
            assert guest["guest_name"] is not None
            assert guest["email"] is not None
            assert "@" in guest["email"]

    def test_generate_bulk_guests_programmatically(self):
        """Test generating bulk data with code."""
        guests = GuestDataGenerator.create_bulk_guests(20)

        assert len(guests) == 20

        # All should have required fields
        for guest in guests:
            assert guest["name"] is not None
            assert guest["email"] is not None

    def test_generate_bulk_reservations(self):
        """Test generating bulk reservations."""
        reservations = ReservationDataGenerator.create_bulk_reservations(15)

        assert len(reservations) == 15

        # Verify date logic
        from datetime import datetime

        for res in reservations:
            arrival = datetime.fromisoformat(res["arrival_date"])
            departure = datetime.fromisoformat(res["departure_date"])
            assert departure > arrival


class TestDataScenarios:
    """Examples of complex test data scenarios."""

    def test_complete_booking_scenario(self):
        """Test building complete booking scenario."""
        # Use builder pattern to create complete test scenario
        scenario = (
            create_test_scenario()
            .with_vip_guest()
            .with_reservation(room_type="SUITE", adults=2)
            .with_room(status="VA")
            .with_payment(499.00)
            .build()
        )

        # Verify scenario
        assert scenario["guest"]["vip_status"] == "platinum"
        assert scenario["reservation"]["room_type"] == "SUITE"
        assert scenario["room"]["status"] == "VA"
        assert len(scenario["payments"]) == 1
        assert scenario["payments"][0]["amount"] == 499.00

    def test_multiple_scenarios(self):
        """Test creating multiple scenarios."""
        scenarios = []

        # Create multiple scenarios for testing
        for i in range(5):
            scenario = (
                create_test_scenario()
                .with_guest(name=f"Test Guest {i}")
                .with_reservation(guest_name=f"Test Guest {i}", room_type="DELUXE")
                .build()
            )
            scenarios.append(scenario)

        assert len(scenarios) == 5

        # Verify uniqueness
        names = [s["guest"]["name"] for s in scenarios]
        assert len(set(names)) == 5  # All unique

    def test_parametrized_with_scenarios(self, various_guest_types):
        """Test with parametrized data."""
        # various_guest_types fixture automatically runs this test
        # for each guest type: valid, vip, corporate, international

        assert various_guest_types["name"] is not None
        assert various_guest_types["email"] is not None

        # Test will run 4 times (once for each guest type)


class TestDataValidation:
    """Examples of data validation testing."""

    @pytest.mark.parametrize(
        "email,expected_valid",
        [
            ("user@example.com", True),
            ("user.name@example.com", True),
            ("user+tag@example.com", True),
            ("not-an-email", False),
            ("@example.com", False),
            ("user@", False),
            ("", False),
        ],
    )
    def test_email_validation(self, email, expected_valid):
        """Test email validation with various inputs."""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        is_valid = bool(re.match(pattern, email))

        assert is_valid == expected_valid

    @pytest.mark.parametrize(
        "adults,children,expected_valid",
        [
            (1, 0, True),  # Valid: 1 adult
            (2, 2, True),  # Valid: family
            (0, 0, False),  # Invalid: no guests
            (5, 0, False),  # Invalid: too many adults
            (2, 4, False),  # Invalid: too many children
        ],
    )
    def test_guest_count_validation(self, adults, children, expected_valid):
        """Test guest count validation."""
        # Assuming max occupancy is 4 adults and 3 children
        max_adults = 4
        max_children = 3

        is_valid = (
            adults >= 1 and adults <= max_adults and children >= 0 and children <= max_children
        )

        assert is_valid == expected_valid


class TestDataCleanup:
    """Examples of test data cleanup."""

    def test_with_cleanup_tracking(self, cleanup_tracker):
        """Test using cleanup tracker."""
        # Create test data
        guest_id = "GUEST-001"
        reservation_id = "RES-001"

        # Track for cleanup
        cleanup_tracker["guests"].append(guest_id)
        cleanup_tracker["reservations"].append(reservation_id)

        # Perform test
        assert guest_id is not None
        assert reservation_id is not None

        # Cleanup would happen here (in real test)
        # This is just demonstrating the tracking mechanism


class TestDataModification:
    """Examples of modifying test data."""

    def test_merge_base_with_overrides(self, valid_guest):
        """Test merging base data with overrides."""
        from tests.fixtures.data_fixtures import merge_dicts

        # Start with base data
        base = valid_guest

        # Override specific fields
        overrides = {"email": "custom@email.com", "country": "Canada"}

        # Merge
        modified = merge_dicts(base, overrides)

        # Verify
        assert modified["name"] == base["name"]  # Original preserved
        assert modified["email"] == "custom@email.com"  # Overridden
        assert modified["country"] == "Canada"  # Added

    def test_dynamic_data_modification(self, random_guest):
        """Test dynamically modifying generated data."""
        # Start with random guest
        guest = random_guest.copy()

        # Modify for specific test scenario
        guest["vip_status"] = "gold"
        guest["loyalty_points"] = 5000

        # Test with modified data
        assert guest["vip_status"] == "gold"
        assert guest["loyalty_points"] == 5000


# ============================================================================
# Running These Tests
# ============================================================================

"""
To run these example tests:

# Run all example tests
pytest src/tests/examples/test_data_examples.py -v

# Run specific test class
pytest src/tests/examples/test_data_examples.py::TestGuestCreation -v

# Run with specific marker
pytest -m parametrize -v

# Run with verbose output
pytest src/tests/examples/test_data_examples.py -vv -s

# Generate Allure report
pytest src/tests/examples/test_data_examples.py --alluredir=allure-results
allure serve allure-results
"""

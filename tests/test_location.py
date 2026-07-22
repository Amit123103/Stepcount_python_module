"""Unit tests for location module."""

from stepdistance.location import Location


def test_location_creation():
    loc = Location(name="Delhi")
    assert loc.name == "Delhi"
    assert str(loc) == "Delhi"
    assert repr(loc) == "Location(name='Delhi')"

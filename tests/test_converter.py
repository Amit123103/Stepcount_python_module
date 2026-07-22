"""Unit tests for converter module."""

import pytest
from stepdistance.converter import feet_to_meters, height_to_meters, km_to_meters, miles_to_meters, to_meters
from stepdistance.utils import InvalidUnitError


def test_km_to_meters():
    assert km_to_meters(1.0) == 1000.0
    assert km_to_meters(233) == 233000.0


def test_miles_to_meters():
    assert pytest.approx(miles_to_meters(1.0), 0.001) == 1609.344


def test_feet_to_meters():
    assert pytest.approx(feet_to_meters(10.0), 0.001) == 3.048


def test_to_meters_dispatcher():
    assert to_meters(5, "km") == 5000.0
    assert to_meters(100, "m") == 100.0
    assert pytest.approx(to_meters(1, "miles"), 0.001) == 1609.344
    assert pytest.approx(to_meters(10, "feet"), 0.001) == 3.048


def test_height_to_meters():
    assert pytest.approx(height_to_meters(175, "cm"), 0.001) == 1.75
    assert pytest.approx(height_to_meters(1.80, "m"), 0.001) == 1.80
    assert pytest.approx(height_to_meters(70, "inches"), 0.001) == 1.778
    assert pytest.approx(height_to_meters(6, "ft"), 0.001) == 1.8288


def test_invalid_unit():
    with pytest.raises(InvalidUnitError):
        to_meters(10, "lightyears")


def test_invalid_negative_distance():
    with pytest.raises(ValueError):
        km_to_meters(-5)

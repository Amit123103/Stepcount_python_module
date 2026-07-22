"""Unit tests for utils module."""

import logging
import pytest
from stepdistance.utils import (
    InvalidDistanceError,
    InvalidStepLengthError,
    InvalidUnitError,
    setup_logging,
    validate_positive,
    validate_unit,
)


def test_validate_positive_valid():
    assert validate_positive(10, "dist") == 10.0
    assert validate_positive(0.5, "dist") == 0.5


def test_validate_positive_invalid():
    with pytest.raises(ValueError):
        validate_positive(0, "dist")

    with pytest.raises(ValueError):
        validate_positive(-5, "dist")

    with pytest.raises(TypeError):
        validate_positive("abc", "dist")


def test_validate_unit():
    assert validate_unit("KM") == "km"
    assert validate_unit("miles ") == "miles"
    with pytest.raises(InvalidUnitError):
        validate_unit("yards")


def test_setup_logging():
    logger = setup_logging(logging.DEBUG)
    assert logger.name == "stepdistance"
    assert logger.level == logging.DEBUG

"""
stepdistance.utils
==================

Utility helpers for the StepDistanceCalculator package.

Provides:
    - Custom exception classes for domain-specific errors.
    - Input-validation helper functions.
    - Centralised logging configuration.
"""

from __future__ import annotations

import logging
from typing import Any

# ---------------------------------------------------------------------------
# Supported distance units (canonical lowercase keys)
# ---------------------------------------------------------------------------
SUPPORTED_UNITS: set[str] = {"m", "km", "miles", "feet"}

# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------


class StepDistanceError(Exception):
    """Base exception for all StepDistanceCalculator errors."""


class InvalidDistanceError(StepDistanceError):
    """Raised when a distance value is invalid (e.g. negative or zero)."""

    def __init__(self, value: Any, message: str | None = None) -> None:
        self.value = value
        super().__init__(
            message or f"Invalid distance value: {value!r}. Must be a positive number."
        )


class InvalidStepLengthError(StepDistanceError):
    """Raised when a step-length value is invalid (e.g. negative or zero)."""

    def __init__(self, value: Any, message: str | None = None) -> None:
        self.value = value
        super().__init__(
            message or f"Invalid step length: {value!r}. Must be a positive number."
        )


class InvalidUnitError(StepDistanceError):
    """Raised when an unsupported distance unit is supplied."""

    def __init__(self, unit: str, message: str | None = None) -> None:
        self.unit = unit
        super().__init__(
            message
            or (
                f"Invalid unit: {unit!r}. "
                f"Supported units: {', '.join(sorted(SUPPORTED_UNITS))}."
            )
        )


# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------


def validate_positive(value: float, name: str = "value") -> float:
    """Validate that *value* is a positive number.

    Parameters
    ----------
    value:
        The numeric value to check.
    name:
        A human-readable label used in error messages.

    Returns
    -------
    float
        The validated value (unchanged).

    Raises
    ------
    TypeError
        If *value* is not ``int`` or ``float``.
    ValueError
        If *value* is less than or equal to zero.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}.")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}.")
    return float(value)


def validate_unit(unit: str) -> str:
    """Validate that *unit* is a supported distance unit.

    Parameters
    ----------
    unit:
        The unit string to validate (case-insensitive).

    Returns
    -------
    str
        The canonical (lowercased) unit string.

    Raises
    ------
    InvalidUnitError
        If the unit is not in :data:`SUPPORTED_UNITS`.
    """
    normalised = unit.strip().lower()
    if normalised not in SUPPORTED_UNITS:
        raise InvalidUnitError(unit)
    return normalised


# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------

_LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)-8s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int | str = logging.INFO) -> logging.Logger:
    """Configure and return the package-level logger.

    Call this once at application startup to set a consistent format and
    level for all ``stepdistance.*`` loggers.

    Parameters
    ----------
    level:
        Logging level — an ``int`` constant (e.g. ``logging.DEBUG``) or a
        string name (e.g. ``"DEBUG"``).

    Returns
    -------
    logging.Logger
        The configured root logger for the ``stepdistance`` namespace.
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    logger = logging.getLogger("stepdistance")
    logger.setLevel(level)

    # Avoid duplicate handlers when called more than once
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
        logger.addHandler(handler)

    return logger

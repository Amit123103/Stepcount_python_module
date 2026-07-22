"""
stepdistance.converter
======================

Distance-unit conversion utilities.

Every public function converts a given value to **meters**, the internal
canonical unit used throughout the package.

Supported units
---------------
* ``m``     — metres (identity)
* ``km``    — kilometres
* ``miles`` — statute miles
* ``feet``  — feet
"""

from __future__ import annotations

import logging
from typing import Final

from stepdistance.utils import validate_positive, validate_unit

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Conversion factors  (1 unit → meters)
# ---------------------------------------------------------------------------
KM_TO_M: Final[float] = 1_000.0
MILES_TO_M: Final[float] = 1_609.344
FEET_TO_M: Final[float] = 0.3048
CM_TO_M: Final[float] = 0.01
INCHES_TO_M: Final[float] = 0.0254

# Lookup table keyed by canonical unit string
_FACTOR: dict[str, float] = {
    "m": 1.0,
    "km": KM_TO_M,
    "miles": MILES_TO_M,
    "feet": FEET_TO_M,
    "ft": FEET_TO_M,
    "cm": CM_TO_M,
    "in": INCHES_TO_M,
    "inches": INCHES_TO_M,
}


# ---------------------------------------------------------------------------
# Individual conversion helpers
# ---------------------------------------------------------------------------


def km_to_meters(km: float) -> float:
    """Convert kilometres to metres.

    Parameters
    ----------
    km:
        Distance in kilometres.  Must be positive.

    Returns
    -------
    float
        Equivalent distance in metres.
    """
    validate_positive(km, "km")
    result = km * KM_TO_M
    logger.debug("Converted %.4f km → %.4f m", km, result)
    return result


def miles_to_meters(miles: float) -> float:
    """Convert statute miles to metres.

    Parameters
    ----------
    miles:
        Distance in miles.  Must be positive.

    Returns
    -------
    float
        Equivalent distance in metres.
    """
    validate_positive(miles, "miles")
    result = miles * MILES_TO_M
    logger.debug("Converted %.4f miles → %.4f m", miles, result)
    return result


def feet_to_meters(feet: float) -> float:
    """Convert feet to metres.

    Parameters
    ----------
    feet:
        Distance in feet.  Must be positive.

    Returns
    -------
    float
        Equivalent distance in metres.
    """
    validate_positive(feet, "feet")
    result = feet * FEET_TO_M
    logger.debug("Converted %.4f feet → %.4f m", feet, result)
    return result


def height_to_meters(height: float, unit: str = "cm") -> float:
    """Convert height value in *unit* to metres.

    Parameters
    ----------
    height:
        Height value. Must be positive.
    unit:
        Height unit (``"cm"``, ``"m"``, ``"in"``, ``"inches"``, ``"ft"``, ``"feet"``).
        Default is ``"cm"``.

    Returns
    -------
    float
        Height converted to metres.
    """
    validate_positive(height, "height")
    u = unit.strip().lower()
    if u not in _FACTOR:
        raise InvalidUnitError(unit, f"Unsupported height unit: {unit!r}.")
    return height * _FACTOR[u]


# ---------------------------------------------------------------------------
# Unified dispatcher
# ---------------------------------------------------------------------------


def to_meters(value: float, unit: str) -> float:
    """Convert *value* in the given *unit* to metres.

    This is the primary conversion entry-point used by the rest of the
    package.  It normalises the unit string and delegates to the
    appropriate conversion factor.

    Parameters
    ----------
    value:
        Numeric distance value.  Must be positive.
    unit:
        One of ``"m"``, ``"km"``, ``"miles"``, ``"feet"``
        (case-insensitive).

    Returns
    -------
    float
        Distance expressed in metres.

    Raises
    ------
    InvalidUnitError
        If *unit* is not recognised.
    ValueError
        If *value* is not positive.
    """
    validate_positive(value, "distance")
    canonical = validate_unit(unit)
    factor = _FACTOR[canonical]
    result = value * factor
    logger.debug("Converted %.4f %s → %.4f m (factor=%.4f)", value, canonical, result, factor)
    return result

"""
stepdistance.person
===================

Defines the :class:`Person` model — the walker whose step length drives
all step-count calculations. Supports height-based biomechanical step length
estimation, stride-length conversions, and pace/activity multiplier adjustments.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Final, Optional

from stepdistance.converter import height_to_meters
from stepdistance.utils import validate_positive

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default step lengths (in metres) based on gender
# ---------------------------------------------------------------------------
DEFAULT_STEP_LENGTH_MALE: Final[float] = 0.78
DEFAULT_STEP_LENGTH_FEMALE: Final[float] = 0.70
DEFAULT_STEP_LENGTH: Final[float] = 0.74  # gender-neutral fallback

# ---------------------------------------------------------------------------
# Height-to-step length factors (biometrically validated)
# Step length (m) = Height (m) * Factor
# ---------------------------------------------------------------------------
HEIGHT_STEP_FACTOR_MALE: Final[float] = 0.415
HEIGHT_STEP_FACTOR_FEMALE: Final[float] = 0.413
HEIGHT_STEP_FACTOR_NEUTRAL: Final[float] = 0.414

# ---------------------------------------------------------------------------
# Pace / Activity multipliers (scale base step length)
# ---------------------------------------------------------------------------
PACE_MULTIPLIERS: dict[str, float] = {
    "walking": 1.00,
    "brisk_walking": 1.08,
    "power_walking": 1.08,
    "jogging": 1.25,
    "running": 1.40,
    "hilly": 0.90,
    "uphill": 0.90,
}


@dataclass
class Person:
    """Represents a person who will walk or run a route.

    Parameters
    ----------
    name:
        Display name of the person.
    step_length:
        Average step length in metres. If *None*, calculated from
        *stride_length*, *height*, or *gender*.
    stride_length:
        Full stride length (distance for 2 steps) in metres.
    gender:
        ``"male"``, ``"female"``, or ``None``.
    height:
        Height of the person in units specified by *height_unit*.
    height_unit:
        Unit of height (``"cm"``, ``"m"``, ``"in"``, ``"ft"``). Default ``"cm"``.
    pace:
        Activity pace mode (``"walking"``, ``"brisk_walking"``, ``"jogging"``,
        ``"running"``, ``"hilly"``). Default ``"walking"``.

    Examples
    --------
    >>> person = Person(name="Amit", step_length=0.75)
    >>> person.step_length
    0.75

    >>> height_person = Person(name="Priya", height=165, height_unit="cm", gender="female")
    >>> round(height_person.step_length, 4)
    0.6815
    """

    name: str
    step_length: Optional[float] = None
    stride_length: Optional[float] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    height_unit: str = "cm"
    pace: str = "walking"

    def __post_init__(self) -> None:
        """Apply defaults and validate after dataclass initialisation."""
        if self.gender is not None:
            self.gender = self.gender.strip().lower()

        if self.pace is not None:
            self.pace = self.pace.strip().lower()
            if self.pace not in PACE_MULTIPLIERS:
                self.pace = "walking"

        # Resolve step length in order of specificity
        if self.step_length is not None:
            validate_positive(self.step_length, "step_length")
        elif self.stride_length is not None:
            validate_positive(self.stride_length, "stride_length")
            self.step_length = self.stride_length / 2.0
            logger.info("Calculated step_length %.4f m from stride_length %.4f m.", self.step_length, self.stride_length)
        elif self.height is not None:
            validate_positive(self.height, "height")
            height_m = height_to_meters(self.height, self.height_unit)
            factor = self._height_factor()
            self.step_length = height_m * factor
            logger.info(
                "Calculated step_length %.4f m from height %.2f %s.",
                self.step_length,
                self.height,
                self.height_unit,
            )
        else:
            self.step_length = self._default_step_length()
            logger.info(
                "No step length or height for %s — defaulting to %.2f m (%s).",
                self.name,
                self.step_length,
                self.gender or "neutral",
            )

    # ----- helpers -----

    def _height_factor(self) -> float:
        """Return the height multiplier factor based on gender."""
        if self.gender == "male":
            return HEIGHT_STEP_FACTOR_MALE
        elif self.gender == "female":
            return HEIGHT_STEP_FACTOR_FEMALE
        return HEIGHT_STEP_FACTOR_NEUTRAL

    def _default_step_length(self) -> float:
        """Return the default static step length based on gender."""
        if self.gender == "male":
            return DEFAULT_STEP_LENGTH_MALE
        elif self.gender == "female":
            return DEFAULT_STEP_LENGTH_FEMALE
        return DEFAULT_STEP_LENGTH

    def get_effective_step_length(self, pace: Optional[str] = None) -> float:
        """Return step length adjusted for the activity pace mode.

        Parameters
        ----------
        pace:
            Activity pace mode name (e.g. ``"jogging"``). If *None*, uses
            ``self.pace``.

        Returns
        -------
        float
            Effective step length in metres.
        """
        p = (pace or self.pace or "walking").strip().lower()
        multiplier = PACE_MULTIPLIERS.get(p, 1.00)
        assert self.step_length is not None
        return self.step_length * multiplier

    # ----- display -----

    def __str__(self) -> str:
        """Human-readable single-line summary."""
        assert self.step_length is not None
        return f"{self.name} (step length: {self.step_length:.2f} m, pace: {self.pace})"

    def summary(self) -> str:
        """Return a multi-line summary suitable for reports.

        Returns
        -------
        str
            Formatted string containing name, height, gender, step length, and pace.
        """
        assert self.step_length is not None
        lines = [
            f"Person       : {self.name}",
            f"Gender       : {self.gender or 'N/A'}",
            f"Height       : {f'{self.height:.1f} {self.height_unit}' if self.height else 'N/A'}",
            f"Step Length   : {self.step_length:.4f} m",
            f"Pace Mode    : {self.pace}",
            f"Effective SL : {self.get_effective_step_length():.4f} m",
        ]
        return "\n".join(lines)

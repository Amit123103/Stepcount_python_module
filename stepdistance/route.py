"""
stepdistance.route
==================

Defines the :class:`Segment` and :class:`Route` models for describing
multi-city walking routes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Iterator, List

from stepdistance.converter import to_meters
from stepdistance.location import Location
from stepdistance.utils import validate_positive, validate_unit

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Segment
# ---------------------------------------------------------------------------


@dataclass
class Segment:
    """A single leg of a walking route.

    Attributes
    ----------
    origin:
        Starting :class:`Location`.
    destination:
        Ending :class:`Location`.
    distance:
        Numeric distance between *origin* and *destination*.
    unit:
        Distance unit (``"m"``, ``"km"``, ``"miles"``, ``"feet"``).
    """

    origin: Location
    destination: Location
    distance: float
    unit: str = "km"

    def __post_init__(self) -> None:
        """Validate fields after dataclass initialisation."""
        validate_positive(self.distance, "segment distance")
        self.unit = validate_unit(self.unit)

    @property
    def distance_meters(self) -> float:
        """Return the segment distance converted to metres."""
        return to_meters(self.distance, self.unit)

    @property
    def label(self) -> str:
        """Return a human-readable label like ``'Delhi -> Agra'``."""
        return f"{self.origin.name} -> {self.destination.name}"

    def __str__(self) -> str:
        """Human-readable segment string."""
        return f"{self.label} : {self.distance:,.2f} {self.unit}"


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------


@dataclass
class Route:
    """An ordered chain of :class:`Segment` objects forming a walking route.

    Examples
    --------
    >>> route = Route()
    >>> route.add_location("Delhi", "Agra", 233)
    >>> route.add_location("Agra", "Jaipur", 238)
    >>> route.segment_count
    2
    """

    segments: List[Segment] = field(default_factory=list)

    # ---- mutators ----

    def add_segment(
        self,
        origin: str,
        destination: str,
        distance: float,
        unit: str = "km",
    ) -> Segment:
        """Create and append a new segment.

        Parameters
        ----------
        origin:
            Name of the starting location.
        destination:
            Name of the ending location.
        distance:
            Distance between the two locations.
        unit:
            Distance unit (default ``"km"``).

        Returns
        -------
        Segment
            The newly created segment.
        """
        seg = Segment(
            origin=Location(name=origin),
            destination=Location(name=destination),
            distance=distance,
            unit=unit,
        )
        self.segments.append(seg)
        logger.info("Added segment: %s", seg)
        return seg

    def add_location(
        self,
        origin: str,
        destination: str,
        distance: float,
        unit: str = "km",
    ) -> Segment:
        """Alias for :meth:`add_segment` (matches prompt API).

        Parameters
        ----------
        origin:
            Name of the starting location.
        destination:
            Name of the ending location.
        distance:
            Distance between the two locations.
        unit:
            Distance unit (default ``"km"``).

        Returns
        -------
        Segment
            The newly created segment.
        """
        return self.add_segment(origin, destination, distance, unit)

    def add_from_tuples(
        self,
        data: list[tuple[str, str, float]],
        unit: str = "km",
    ) -> None:
        """Bulk-add segments from a list of ``(origin, dest, distance)`` tuples.

        Parameters
        ----------
        data:
            List of 3-tuples describing each leg.
        unit:
            Common unit for all entries (default ``"km"``).
        """
        for origin, dest, dist in data:
            self.add_segment(origin, dest, dist, unit)

    # ---- properties ----

    @property
    def segment_count(self) -> int:
        """Return the number of segments in the route."""
        return len(self.segments)

    @property
    def total_distance_meters(self) -> float:
        """Return the total route distance in metres."""
        return sum(seg.distance_meters for seg in self.segments)

    @property
    def total_distance_km(self) -> float:
        """Return the total route distance in kilometres."""
        return self.total_distance_meters / 1_000.0

    def get_segment_percentages(self) -> list[dict[str, float | str]]:
        """Return each segment's percentage contribution to total distance.

        Returns
        -------
        list[dict]
            Each dict contains ``"label"``, ``"distance_m"``, and ``"percentage"``.
        """
        total = self.total_distance_meters
        if total == 0:
            return []
        result: list[dict[str, float | str]] = []
        for seg in self.segments:
            d = seg.distance_meters
            result.append(
                {
                    "label": seg.label,
                    "distance_m": d,
                    "percentage": round((d / total) * 100, 2),
                }
            )
        return result

    # ---- iteration ----

    def __iter__(self) -> Iterator[Segment]:
        """Iterate over segments."""
        return iter(self.segments)

    def __len__(self) -> int:
        """Return the number of segments."""
        return self.segment_count

    # ---- display ----

    def __str__(self) -> str:
        """Return a human-readable route summary."""
        lines = [str(seg) for seg in self.segments]
        lines.append(f"Total distance: {self.total_distance_km:,.2f} km")
        return "\n".join(lines)

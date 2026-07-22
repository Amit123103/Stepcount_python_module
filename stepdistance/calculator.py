"""
stepdistance.calculator
=======================

Core calculation engine. Combines a :class:`Person` and an optional
:class:`Route` to compute step counts, cumulative distances, and
segment-level statistics with support for pace adjustments and flexible rounding modes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from math import ceil, floor
from typing import List, Optional

from stepdistance.converter import to_meters
from stepdistance.person import Person
from stepdistance.route import Route, Segment
from stepdistance.utils import validate_positive

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StepResult:
    """Immutable result of a single step-count calculation.

    Attributes
    ----------
    origin:
        Starting location name.
    destination:
        Ending location name.
    distance_m:
        Distance in metres.
    steps_exact:
        Exact (floating-point) step count.
    steps_rounded:
        Step count rounded according to *rounding_mode*.
    step_length:
        The effective step length (m) used for the calculation.
    pace:
        Pace activity mode used (e.g. ``"walking"``, ``"running"``).
    rounding_mode:
        Rounding mode applied (``"ceil"``, ``"round"``, ``"floor"``, ``"exact"``).
    """

    origin: str
    destination: str
    distance_m: float
    steps_exact: float
    steps_rounded: int
    step_length: float
    pace: str = "walking"
    rounding_mode: str = "ceil"


@dataclass(frozen=True)
class RouteResult:
    """Immutable result of a full route calculation.

    Attributes
    ----------
    person:
        The :class:`Person` who would walk the route.
    segment_results:
        Per-segment :class:`StepResult` objects.
    total_distance_m:
        Total distance in metres.
    total_steps:
        Total rounded step count.
    percentages:
        Per-segment distance percentage contributions.
    cumulative_distances:
        Running total of distance after each segment (metres).
    cumulative_steps:
        Running total of steps after each segment.
    """

    person: Person
    segment_results: list[StepResult]
    total_distance_m: float
    total_steps: int
    percentages: list[dict]
    cumulative_distances: list[float]
    cumulative_steps: list[int]


# ---------------------------------------------------------------------------
# History entry
# ---------------------------------------------------------------------------


@dataclass
class HistoryEntry:
    """A timestamped record of a past calculation."""

    timestamp: str
    person_name: str
    origin: str
    destination: str
    distance_m: float
    steps: int


# ---------------------------------------------------------------------------
# DistanceCalculator
# ---------------------------------------------------------------------------


class DistanceCalculator:
    """Central calculation engine for walking/running step estimates.

    Parameters
    ----------
    person:
        The :class:`Person` performing the walk.
    route:
        An optional pre-built :class:`Route`. Can also be set later.

    Examples
    --------
    >>> from stepdistance.person import Person
    >>> from stepdistance.route import Route
    >>> person = Person(name="Amit", step_length=0.75)
    >>> route = Route()
    >>> route.add_location("Delhi", "Agra", 233)
    >>> calc = DistanceCalculator(person, route)
    >>> result = calc.calculate_route()
    >>> result.total_steps
    310667
    """

    def __init__(self, person: Person, route: Optional[Route] = None) -> None:
        self.person = person
        self.route = route
        self._history: List[HistoryEntry] = []

    # ---- single calculation ----

    def calculate_steps(
        self,
        distance: float,
        unit: str = "m",
        origin: str = "A",
        destination: str = "B",
        pace: Optional[str] = None,
        rounding_mode: str = "ceil",
    ) -> StepResult:
        """Calculate steps for a single distance.

        Parameters
        ----------
        distance:
            Numeric distance value.
        unit:
            Distance unit (default ``"m"``).
        origin:
            Label for the starting point.
        destination:
            Label for the ending point.
        pace:
            Optional activity pace override (e.g. ``"jogging"``).
            If *None*, defaults to ``self.person.pace``.
        rounding_mode:
            Step integer rounding strategy (``"ceil"``, ``"round"``,
            ``"floor"``, ``"exact"``). Default is ``"ceil"``.

        Returns
        -------
        StepResult
            Calculation outcome.
        """
        distance_m = to_meters(distance, unit)
        effective_pace = (pace or self.person.pace or "walking").strip().lower()
        effective_step_len = self.person.get_effective_step_length(effective_pace)

        steps_exact = distance_m / effective_step_len

        mode = rounding_mode.strip().lower()
        if mode == "round":
            steps_rounded = int(round(steps_exact))
        elif mode == "floor":
            steps_rounded = int(floor(steps_exact))
        elif mode == "exact":
            steps_rounded = int(round(steps_exact))
        else:  # default "ceil"
            steps_rounded = ceil(steps_exact)

        result = StepResult(
            origin=origin,
            destination=destination,
            distance_m=distance_m,
            steps_exact=steps_exact,
            steps_rounded=steps_rounded,
            step_length=effective_step_len,
            pace=effective_pace,
            rounding_mode=mode,
        )

        # Record in history
        self._record(result)
        logger.info(
            "%s -> %s : %.0f m (%s) -> %s steps",
            origin,
            destination,
            distance_m,
            effective_pace,
            f"{steps_rounded:,}",
        )
        return result

    # ---- route calculation ----

    def calculate_route(
        self,
        route: Optional[Route] = None,
        pace: Optional[str] = None,
        rounding_mode: str = "ceil",
    ) -> RouteResult:
        """Calculate step counts for every segment in a route.

        Parameters
        ----------
        route:
            The route to process. Falls back to ``self.route``.
        pace:
            Optional activity pace override for all segments.
        rounding_mode:
            Step rounding mode applied to each segment.

        Returns
        -------
        RouteResult
            Aggregated results for the entire route.

        Raises
        ------
        ValueError
            If no route is available.
        """
        r = route or self.route
        if r is None or r.segment_count == 0:
            raise ValueError("No route provided or route has no segments.")

        segment_results: list[StepResult] = []
        cumulative_dist: list[float] = []
        cumulative_steps_list: list[int] = []
        running_dist = 0.0
        running_steps = 0

        for seg in r:
            sr = self.calculate_steps(
                distance=seg.distance,
                unit=seg.unit,
                origin=seg.origin.name,
                destination=seg.destination.name,
                pace=pace,
                rounding_mode=rounding_mode,
            )
            segment_results.append(sr)
            running_dist += sr.distance_m
            running_steps += sr.steps_rounded
            cumulative_dist.append(running_dist)
            cumulative_steps_list.append(running_steps)

        total_dist = running_dist
        total_steps = running_steps
        percentages = r.get_segment_percentages()

        return RouteResult(
            person=self.person,
            segment_results=segment_results,
            total_distance_m=total_dist,
            total_steps=total_steps,
            percentages=percentages,
            cumulative_distances=cumulative_dist,
            cumulative_steps=cumulative_steps_list,
        )

    # ---- history ----

    def _record(self, result: StepResult) -> None:
        """Append a result to the internal history list."""
        entry = HistoryEntry(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            person_name=self.person.name,
            origin=result.origin,
            destination=result.destination,
            distance_m=result.distance_m,
            steps=result.steps_rounded,
        )
        self._history.append(entry)

    def get_history(self) -> list[HistoryEntry]:
        """Return a copy of the calculation history.

        Returns
        -------
        list[HistoryEntry]
            All past calculations performed by this calculator instance.
        """
        return list(self._history)

    def clear_history(self) -> None:
        """Clear the calculation history."""
        self._history.clear()
        logger.info("Calculation history cleared.")

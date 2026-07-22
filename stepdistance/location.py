"""
stepdistance.location
=====================

Defines the :class:`Location` model — a lightweight representation of a
named place.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """Immutable representation of a named geographical location.

    Parameters
    ----------
    name:
        The display name of the location (e.g. ``"Delhi"``).

    Examples
    --------
    >>> loc = Location(name="Agra")
    >>> str(loc)
    'Agra'
    """

    name: str

    def __str__(self) -> str:
        """Return the location name."""
        return self.name

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Location(name={self.name!r})"

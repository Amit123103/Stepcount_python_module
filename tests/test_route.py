"""Unit tests for route module."""

import pytest
from stepdistance.route import Route, Segment


def test_add_segment():
    r = Route()
    seg = r.add_segment("Delhi", "Agra", 233, unit="km")
    assert r.segment_count == 1
    assert seg.origin.name == "Delhi"
    assert seg.destination.name == "Agra"
    assert seg.distance_meters == 233000.0


def test_add_location_alias():
    r = Route()
    seg = r.add_location("Agra", "Jaipur", 238)
    assert r.segment_count == 1
    assert seg.distance == 238


def test_total_distance():
    r = Route()
    r.add_segment("Delhi", "Agra", 233, "km")
    r.add_segment("Agra", "Jaipur", 238, "km")
    assert r.total_distance_km == 471.0
    assert r.total_distance_meters == 471000.0


def test_segment_percentages():
    r = Route()
    r.add_segment("A", "B", 100, "km")
    r.add_segment("B", "C", 300, "km")
    pcts = r.get_segment_percentages()
    assert len(pcts) == 2
    assert pcts[0]["percentage"] == 25.0
    assert pcts[1]["percentage"] == 75.0


def test_route_iteration():
    r = Route()
    r.add_segment("A", "B", 10)
    r.add_segment("B", "C", 20)
    segs = list(r)
    assert len(segs) == 2
    assert segs[0].origin.name == "A"

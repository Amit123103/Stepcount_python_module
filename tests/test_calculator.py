"""Unit tests for calculator module."""

import pytest
from stepdistance.calculator import DistanceCalculator
from stepdistance.person import Person
from stepdistance.route import Route


def test_single_distance_calculation():
    person = Person(name="Amit", step_length=0.75)
    calc = DistanceCalculator(person=person)

    # 233 km = 233,000 meters / 0.75 step length = 310,666.666... -> ceil 310,667
    res = calc.calculate_steps(233, unit="km", origin="Delhi", destination="Agra")
    assert res.distance_m == 233000.0
    assert pytest.approx(res.steps_exact, 0.001) == 310666.6666
    assert res.steps_rounded == 310667


def test_rounding_modes():
    person = Person(name="Amit", step_length=0.75)
    calc = DistanceCalculator(person=person)

    # 10 meters / 0.75 = 13.3333 steps
    res_ceil = calc.calculate_steps(10, unit="m", rounding_mode="ceil")
    assert res_ceil.steps_rounded == 14

    res_round = calc.calculate_steps(10, unit="m", rounding_mode="round")
    assert res_round.steps_rounded == 13

    res_floor = calc.calculate_steps(10, unit="m", rounding_mode="floor")
    assert res_floor.steps_rounded == 13


def test_pace_calculation():
    person = Person(name="Rohan", height=180, gender="male", pace="jogging")
    # height 180cm male -> step_length = 0.747m, jogging factor = 1.25 -> effective SL = 0.93375m
    calc = DistanceCalculator(person=person)
    res = calc.calculate_steps(1000, unit="m")
    # 1000 / 0.93375 = 1070.95 -> 1071 ceil steps
    assert res.pace == "jogging"
    assert res.steps_rounded == 1071


def test_route_calculation():
    person = Person(name="Amit", step_length=0.75)
    route = Route()
    route.add_location("Delhi", "Agra", 233)
    route.add_location("Agra", "Jaipur", 238)
    route.add_location("Jaipur", "Udaipur", 394)

    calc = DistanceCalculator(person=person, route=route)
    res = calc.calculate_route()

    assert res.total_distance_m == 865000.0
    assert len(res.segment_results) == 3
    assert res.total_steps == sum(sr.steps_rounded for sr in res.segment_results)


def test_history_tracking():
    person = Person(name="Amit", step_length=0.75)
    calc = DistanceCalculator(person=person)

    calc.calculate_steps(100, "m", "A", "B")
    calc.calculate_steps(200, "m", "B", "C")

    history = calc.get_history()
    assert len(history) == 2
    assert history[0].origin == "A"
    assert history[1].origin == "B"

    calc.clear_history()
    assert len(calc.get_history()) == 0

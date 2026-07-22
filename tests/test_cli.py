"""
tests.test_cli
==============

Unit tests for the CLI and interactive menu module.
"""

import sys
from unittest.mock import patch
import pytest

from stepdistance.cli import main, _prompt_person, _prompt_add_segment
from stepdistance.route import Route


def test_prompt_person_male():
    inputs = iter(["TestUser", "1", "1"])  # Name, Male default, Walking
    with patch("builtins.input", lambda _: next(inputs)):
        person = _prompt_person()
        assert person.name == "TestUser"
        assert person.gender == "male"
        assert person.step_length == 0.78
        assert person.pace == "walking"


def test_prompt_person_height():
    inputs = iter(["Priya", "3", "2", "165", "female"])  # Name, Height mode, Brisk walking, 165cm, female
    with patch("builtins.input", lambda _: next(inputs)):
        person = _prompt_person()
        assert person.name == "Priya"
        assert person.height == 165.0
        assert person.gender == "female"
        assert person.pace == "brisk_walking"


def test_prompt_add_segment():
    route = Route()
    inputs = iter(["Delhi", "Agra", "233", "km"])
    with patch("builtins.input", lambda _: next(inputs)):
        success = _prompt_add_segment(route)
        assert success is True
        assert route.segment_count == 1
        assert route.segments[0].origin.name == "Delhi"
        assert route.segments[0].destination.name == "Agra"
        assert route.segments[0].distance == 233.0
        assert route.segments[0].unit == "km"


def test_cli_calculate_command(capsys):
    test_args = [
        "stepdistance",
        "calculate",
        "--from", "Delhi",
        "--to", "Agra",
        "--distance", "233",
        "--unit", "km",
        "--person", "Amit",
        "--step-length", "0.75",
        "--pace", "brisk_walking",
    ]
    with patch.object(sys, "argv", test_args):
        main()
        captured = capsys.readouterr()
        assert "Delhi -> Agra" in captured.out
        assert "Steps Required:" in captured.out

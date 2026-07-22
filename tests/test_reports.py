"""Unit tests for reports module."""

import json
import os
import tempfile
import pytest
from stepdistance.calculator import DistanceCalculator
from stepdistance.person import Person
from stepdistance.reports import ReportGenerator
from stepdistance.route import Route


@pytest.fixture
def sample_route_result():
    person = Person(name="Amit", step_length=0.75)
    route = Route()
    route.add_location("Delhi", "Agra", 233)
    route.add_location("Agra", "Jaipur", 238)
    calc = DistanceCalculator(person=person, route=route)
    return calc.calculate_route()


def test_generate_text(sample_route_result):
    rg = ReportGenerator(sample_route_result)
    text = rg.generate_text()
    assert "Amit" in text
    assert "Delhi -> Agra" in text
    assert "Agra -> Jaipur" in text
    assert "Total Distance" in text


def test_save_json(sample_route_result):
    rg = ReportGenerator(sample_route_result)
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = os.path.join(tmpdir, "report.json")
        saved = rg.save_json(json_path)
        assert os.path.exists(saved)

        with open(saved, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["person"]["name"] == "Amit"
        assert len(data["segments"]) == 2


def test_save_csv(sample_route_result):
    rg = ReportGenerator(sample_route_result)
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "report.csv")
        saved = rg.save_csv(csv_path)
        assert os.path.exists(saved)

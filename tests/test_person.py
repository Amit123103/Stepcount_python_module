"""Unit tests for person module."""

import pytest
from stepdistance.person import (
    DEFAULT_STEP_LENGTH,
    DEFAULT_STEP_LENGTH_FEMALE,
    DEFAULT_STEP_LENGTH_MALE,
    Person,
)


def test_person_explicit_step_length():
    p = Person(name="Amit", step_length=0.75)
    assert p.name == "Amit"
    assert p.step_length == 0.75


def test_person_male_default():
    p = Person(name="Raj", gender="male")
    assert p.step_length == DEFAULT_STEP_LENGTH_MALE


def test_person_female_default():
    p = Person(name="Priya", gender="female")
    assert p.step_length == DEFAULT_STEP_LENGTH_FEMALE


def test_person_neutral_default():
    p = Person(name="Alex")
    assert p.step_length == DEFAULT_STEP_LENGTH


def test_invalid_step_length():
    with pytest.raises(ValueError):
        Person(name="Test", step_length=-0.5)


def test_person_height_male_cm():
    p = Person(name="Vikram", height=180, height_unit="cm", gender="male")
    # 1.80m * 0.415 = 0.747m
    assert pytest.approx(p.step_length, 0.001) == 0.747


def test_person_height_female_cm():
    p = Person(name="Neha", height=165, height_unit="cm", gender="female")
    # 1.65m * 0.413 = 0.68145m
    assert pytest.approx(p.step_length, 0.0001) == 0.68145


def test_person_stride_length():
    p = Person(name="Rahul", stride_length=1.50)
    assert p.step_length == 0.75


def test_person_pace_multipliers():
    p = Person(name="Karan", step_length=0.80, pace="jogging")
    # 0.80 * 1.25 = 1.00
    assert pytest.approx(p.get_effective_step_length(), 0.001) == 1.00
    # Override pace
    assert pytest.approx(p.get_effective_step_length("running"), 0.001) == 1.12  # 0.80 * 1.40


def test_person_summary():
    p = Person(name="Amit", step_length=0.75, gender="male")
    summary = p.summary()
    assert "Amit" in summary
    assert "0.75" in summary

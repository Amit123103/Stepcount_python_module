"""
StepDistanceCalculator
======================

A professional Python module to calculate walking step counts between places
or cities based on total distance and average step length.
"""

from stepdistance.calculator import DistanceCalculator, RouteResult, StepResult
from stepdistance.converter import (
    feet_to_meters,
    km_to_meters,
    miles_to_meters,
    to_meters,
)
from stepdistance.location import Location
from stepdistance.person import (
    DEFAULT_STEP_LENGTH_FEMALE,
    DEFAULT_STEP_LENGTH_MALE,
    Person,
)
from stepdistance.reports import ReportGenerator
from stepdistance.route import Route, Segment
from stepdistance.utils import (
    InvalidDistanceError,
    InvalidStepLengthError,
    InvalidUnitError,
    StepDistanceError,
    setup_logging,
)
from stepdistance.visualization import (
    plot_all,
    plot_cumulative_line,
    plot_distance_pie,
    plot_steps_bar,
)

__version__ = "1.0.0"
__author__ = "StepDistanceCalculator Team"

__all__ = [
    # Core Classes
    "Person",
    "Location",
    "Segment",
    "Route",
    "DistanceCalculator",
    "StepResult",
    "RouteResult",
    "ReportGenerator",
    # Converter
    "km_to_meters",
    "miles_to_meters",
    "feet_to_meters",
    "to_meters",
    # Visualization
    "plot_steps_bar",
    "plot_distance_pie",
    "plot_cumulative_line",
    "plot_all",
    # Utils & Exceptions
    "setup_logging",
    "StepDistanceError",
    "InvalidDistanceError",
    "InvalidStepLengthError",
    "InvalidUnitError",
    # Defaults
    "DEFAULT_STEP_LENGTH_MALE",
    "DEFAULT_STEP_LENGTH_FEMALE",
]

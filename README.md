# StepDistanceCalculator

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/StepDistanceCalculator/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/StepDistanceCalculator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

StepDistanceCalculator is a Python package designed to calculate walking step counts between locations, places, or cities based on total distance, unit conversion, activity pace modes, and biomechanically accurate step length estimation.

---

## Overview

StepDistanceCalculator provides a high-level Python API and Command-Line Interface (CLI) to convert physical distances into step counts. It supports biometric calculations based on height and gender, custom stride/step lengths, activity pace modifiers, multi-segment routes, tabular reports (Text, JSON, CSV, PDF), and Matplotlib visualizations.

---

## Key Features

- Single and Multi-Segment Route Calculations: Compute exact and rounded step counts for single journeys or complex multi-city itineraries.
- Biomechanical Step Length Estimation:
  - Height-Based Estimation: Automatically calculates step length using validated height-to-step ratios (`Step Length = Height × Gender Factor`).
  - Gender Defaults: Pre-configured averages for males (0.78 m), females (0.70 m), and neutral fallbacks (0.74 m).
  - Stride Support: Convert full 2-step stride lengths into single step metrics.
  - Activity Pace Modifiers: Multipliers for Walking (1.00x), Brisk Walking (1.08x), Jogging (1.25x), Running (1.40x), and Hilly/Uphill terrain (0.90x).
- Flexible Unit Support: Converts distance from kilometers (`km`), miles (`miles`), feet (`ft`), meters (`m`), centimeters (`cm`), and inches (`in`).
- Configurable Rounding Modes: Supports `ceil` (default), `floor`, `round`, and `exact` step calculations.
- Comprehensive Reporting: Export structured calculations into Plain Text, JSON, CSV, and PDF formats.
- Data Visualizations: Built-in Matplotlib chart utilities generating segment step bar charts, distance pie charts, and cumulative progress line charts.
- Interactive CLI: Built-in terminal user interface and subcommand arguments.

---

## Installation

### Installation via PyPI

To install the latest release from PyPI:

```bash
pip install StepDistanceCalculator
```

### Installation from Source

To install the package locally for development:

```bash
git clone https://github.com/Amit123103/Stepcount_python_module.git
cd Stepcount_python_module
pip install -e .
```

---

## PyPI Publishing Guide

To publish this package to PyPI manually or via automated pipelines, follow these steps:

### Prerequisites

Ensure `build` and `twine` are installed:

```bash
pip install build twine
```

### 1. Build Source and Wheel Distributions

Clean old build artifacts and generate new distribution archives:

```bash
python -m build
```

This creates a `.tar.gz` source distribution and a `.whl` wheel file inside the `dist/` directory.

### 2. Check Package Validity

Run Twine's check to ensure metadata and long description render correctly:

```bash
twine check dist/*
```

### 3. Upload to TestPyPI (Optional Verification)

Upload the package archives to TestPyPI first:

```bash
twine upload --repository testpypi dist/*
```

### 4. Upload to Production PyPI

Upload the package archives to the official PyPI registry:

```bash
twine upload dist/*
```

Enter your PyPI API token when prompted.

---

## API Reference

### `stepdistance.Person`

Represents an individual walker or runner.

```python
Person(
    name: str,
    step_length: Optional[float] = None,
    stride_length: Optional[float] = None,
    gender: Optional[str] = None,
    height: Optional[float] = None,
    height_unit: str = "cm",
    pace: str = "walking"
)
```

- `step_length`: Step length in meters. If omitted, calculated automatically from stride, height, or gender defaults.
- `stride_length`: Two-step stride length in meters.
- `height`: Height value in specified `height_unit`.
- `height_unit`: `"cm"`, `"m"`, `"in"`, or `"ft"`. Default is `"cm"`.
- `gender`: `"male"`, `"female"`, or `None`.
- `pace`: `"walking"`, `"brisk_walking"`, `"jogging"`, `"running"`, or `"hilly"`.
- `get_effective_step_length(pace: Optional[str] = None) -> float`: Returns the step length scaled by the activity multiplier.
- `summary() -> str`: Returns a formatted text summary of person attributes.

### `stepdistance.Location`

Represents a named geographic location or landmark.

```python
Location(name: str)
```

### `stepdistance.Segment`

Represents a route leg between an origin location and a destination location.

```python
Segment(
    origin: Location | str,
    destination: Location | str,
    distance: float,
    unit: str = "km"
)
```

- `distance_in_meters() -> float`: Returns distance converted into meters.

### `stepdistance.Route`

Collection of connected route segments.

```python
Route()
```

- `add_segment(segment: Segment) -> None`: Appends a `Segment` instance.
- `add_location(origin: str, destination: str, distance: float, unit: str = "km") -> Segment`: Helper method to create and append a segment.
- `total_distance_meters() -> float`: Sum of all segment distances in meters.
- `clear() -> None`: Empties all segments.

### `stepdistance.DistanceCalculator`

Core calculation engine.

```python
DistanceCalculator(person: Person, route: Optional[Route] = None)
```

- `calculate_steps(distance: float, unit: str = "km", origin: str = "", destination: str = "", pace: Optional[str] = None, rounding: str = "ceil") -> StepResult`: Calculates steps for a single distance.
- `calculate_route(rounding: str = "ceil") -> RouteResult`: Calculates step counts across all segments in the attached `Route`.

### `stepdistance.StepResult` & `stepdistance.RouteResult`

Data structures containing calculation outputs including exact step counts (`steps_exact`), rounded step counts (`steps_rounded`), effective step length, and total distance in meters.

### `stepdistance.ReportGenerator`

Generates structured reports for a `RouteResult` or `StepResult`.

```python
ReportGenerator(result: RouteResult | StepResult)
```

- `generate_text() -> str`: Generates formatted text report.
- `generate_json() -> str`: Returns JSON string representation.
- `save_json(filepath: str) -> None`: Writes JSON report to file.
- `save_csv(filepath: str) -> None`: Exports segment breakdown to CSV.
- `save_pdf(filepath: str) -> None`: Generates a PDF summary report.

### `stepdistance.visualization`

Matplotlib plotting utilities:

- `plot_steps_bar(route_result, filename=None, show=False)`: Creates bar chart of steps per segment.
- `plot_distance_pie(route_result, filename=None, show=False)`: Creates pie chart of distance distribution.
- `plot_cumulative_line(route_result, filename=None, show=False)`: Creates cumulative step count progress line chart.
- `plot_all(route_result, save_dir="charts")`: Generates and saves all three charts.

---

## Complete Information and Use Cases

### 1. Basic Single Distance Calculation

Calculate the steps required to walk from Delhi to Agra:

```python
from stepdistance import Person, DistanceCalculator

person = Person(name="Amit", step_length=0.75, pace="brisk_walking")
calc = DistanceCalculator(person=person)

result = calc.calculate_steps(
    distance=233,
    unit="km",
    origin="Delhi",
    destination="Agra"
)

print(f"Route           : {result.origin} -> {result.destination}")
print(f"Distance        : {result.distance_m:,.0f} m")
print(f"Step Length     : {result.step_length:.4f} m")
print(f"Steps Required  : {result.steps_rounded:,}")
```

### 2. Height-Based Biomechanical Calculation

Calculate step count dynamically estimated from user height and gender:

```python
from stepdistance import Person, DistanceCalculator

# Biomechanical calculation: Height 175 cm, Male -> Step length = 1.75 * 0.415 = ~0.7263 m
person = Person(name="Rahul", height=175, height_unit="cm", gender="male", pace="walking")
calc = DistanceCalculator(person=person)

result = calc.calculate_steps(distance=5, unit="km", origin="Home", destination="Park")
print(f"Calculated Step Length : {person.step_length:.4f} m")
print(f"Total Steps            : {result.steps_rounded:,}")
```

### 3. Multi-City Itinerary and Report Generation

Calculate multi-leg trips and export reports:

```python
from stepdistance import Person, Route, DistanceCalculator, ReportGenerator

person = Person(name="Amit", height=178, height_unit="cm", gender="male", pace="walking")

route = Route()
route.add_location("Delhi", "Agra", 233, unit="km")
route.add_location("Agra", "Jaipur", 238, unit="km")
route.add_location("Jaipur", "Udaipur", 394, unit="km")

calc = DistanceCalculator(person=person, route=route)
route_result = calc.calculate_route()

# Console Report
report_gen = ReportGenerator(route_result)
print(report_gen.generate_text())

# Export Files
report_gen.save_json("route_report.json")
report_gen.save_csv("route_report.csv")
report_gen.save_pdf("route_report.pdf")
```

### 4. Graph Visualizations

Generate graphical charts for route step distribution:

```python
from stepdistance import plot_all

chart_files = plot_all(route_result, save_dir="./output_charts")
for file in chart_files:
    print(f"Generated chart: {file}")
```

### 5. Exception Handling

Handle invalid inputs cleanly using custom package exceptions:

```python
from stepdistance import Person, DistanceCalculator, StepDistanceError, InvalidDistanceError

person = Person(name="Test User", step_length=0.75)
calc = DistanceCalculator(person=person)

try:
    calc.calculate_steps(distance=-50, unit="km")
except InvalidDistanceError as e:
    print(f"Distance validation failed: {e}")
except StepDistanceError as e:
    print(f"StepDistance processing error: {e}")
```

---

## CLI and Interactive Console

### Interactive Menu Mode

Launch the interactive console menu:

```bash
stepdistance interactive
```

Interactive choices include single distance calculation, multi-segment route builder, report exporter (JSON, CSV, PDF), graph generator, and profile configuration.

### CLI Subcommands

Calculate a single distance:

```bash
stepdistance calculate --from Delhi --to Agra --distance 233 --unit km --height 175 --gender male --pace brisk_walking
```

Calculate steps from a route JSON specification:

```bash
stepdistance route --file route.json --output-dir ./output
```

---

## Running Tests

Run unit tests using pytest:

```bash
pytest tests/ -v
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# StepDistanceCalculator

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/StepDistanceCalculator/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/StepDistanceCalculator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

StepDistanceCalculator is a professional, object-oriented Python package designed to calculate walking step counts between locations, places, or cities based on total distance, unit conversion, activity pace modes, and biomechanically accurate step length estimation.

---

## Overview

StepDistanceCalculator provides a high-level Python API and Command-Line Interface (CLI) to convert physical distances into precise step counts. It supports biometric calculations based on height and gender, custom stride/step lengths, activity pace modifiers, multi-segment routes, tabular reports (Text, JSON, CSV, PDF), and Matplotlib visualizations.

---

## Features

- Single and Multi-City Calculations: Compute exact and rounded step counts for single routes or multi-segment route chains.
- Default and Custom Step Lengths:
  - Gender Defaults: Pre-configured averages for Adult Males (0.78 m), Adult Females (0.70 m), and Neutral fallbacks (0.74 m).
  - Biomechanical Height Estimation: Calculates step length using validated height-to-step ratios (`Step Length = Height × Gender Factor`).
  - Stride Support: Convert full 2-step stride lengths into single step metrics.
  - Activity Pace Modifiers: Multipliers for Walking (1.00x), Brisk Walking (1.08x), Jogging (1.25x), Running (1.40x), and Hilly/Uphill terrain (0.90x).
- Automatic Unit Conversion: Seamlessly converts distances in meters (`m`), kilometers (`km`), miles (`miles`), feet (`ft`), centimeters (`cm`), and inches (`in`).
- Clean Object-Oriented Design: Built around core domain abstractions including `Person`, `Location`, `Segment`, `Route`, `DistanceCalculator`, and `ReportGenerator`.
- Comprehensive Reports: Export calculation summaries as Plain Text, JSON, CSV, or formatted PDF documents.
- Data Visualizations: Generate Matplotlib charts for segment steps (bar chart), percentage distance contribution (pie chart), and cumulative steps across checkpoints (line chart).
- CLI and Interactive Mode: Built-in Command Line Interface with an interactive terminal menu program.
- Robust and Validated: Complete input validation, custom exception hierarchy, and structured logging.

---

## Project Structure

```text
StepDistanceCalculator/
│
├── stepdistance/            # Core package
│   ├── __init__.py          # Package exports & versioning
│   ├── person.py            # Person class (name, gender, step length, pace)
│   ├── location.py          # Location data class
│   ├── route.py             # Route and Segment classes
│   ├── calculator.py        # DistanceCalculator & result dataclasses
│   ├── converter.py         # Unit conversion module
│   ├── reports.py           # ReportGenerator (Text, JSON, CSV, PDF)
│   ├── visualization.py     # Matplotlib charts (Bar, Pie, Line)
│   ├── utils.py             # Validators, logging & custom exceptions
│   └── cli.py               # CLI & Interactive Menu Program
│
├── examples/                # Example scripts
│   ├── basic_usage.py       # Single distance calculation
│   ├── multi_city.py        # Multi-city route calculation
│   └── generate_reports.py  # Exporting JSON/CSV/PDF & Charts
│
├── tests/                   # Pytest test suite
│   ├── test_calculator.py
│   ├── test_cli.py
│   ├── test_converter.py
│   ├── test_location.py
│   ├── test_person.py
│   ├── test_reports.py
│   ├── test_route.py
│   └── test_utils.py
│
├── docs/
│   └── usage_guide.md
├── pyproject.toml           # Build configuration
├── setup.py                 # Setup script
├── requirements.txt         # Package dependencies
└── README.md
```

---

## Quick Start & Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install StepDistanceCalculator
```

### Option 2: Install from Source / Local Development

Clone the repository and install in editable mode:

```bash
git clone https://github.com/Amit123103/Stepcount_python_module.git
cd Stepcount_python_module
pip install -e .
```

Or install requirements directly:

```bash
pip install -r requirements.txt
```

---

## Python Usage Examples

### 1. Basic Single Distance Calculation

Calculate steps required to walk between two cities with a custom step length:

```python
from stepdistance import Person, DistanceCalculator

person = Person(name="Amit", step_length=0.75, pace="brisk_walking")
calc = DistanceCalculator(person=person)

result = calc.calculate_steps(distance=233, unit="km", origin="Delhi", destination="Agra")

print(f"Origin         : {result.origin}")
print(f"Destination    : {result.destination}")
print(f"Distance (m)   : {result.distance_m:,.0f} m")
print(f"Effective SL   : {result.step_length:.4f} m")
print(f"Steps Required : {result.steps_rounded:,}")
# Output: Steps Required: 287,655
```

### 2. Height-Based Biomechanical Step Calculation

Calculate step count dynamically estimated from height and gender:

```python
from stepdistance import Person, DistanceCalculator

# Height: 175 cm, Gender: Male -> Step length calculated automatically (~0.7263 m)
person = Person(name="Rahul", height=175, height_unit="cm", gender="male", pace="walking")
calc = DistanceCalculator(person=person)

result = calc.calculate_steps(distance=5, unit="km", origin="Home", destination="Park")

print(f"Calculated Step Length : {person.step_length:.4f} m")
print(f"Total Steps            : {result.steps_rounded:,}")
```

### 3. Multi-City Route Chain

Build a multi-segment route and calculate total step metrics:

```python
from stepdistance import Person, Route, DistanceCalculator, ReportGenerator

person = Person(name="Amit", step_length=0.75)

route = Route()
route.add_location("Delhi", "Agra", 233, unit="km")
route.add_location("Agra", "Jaipur", 238, unit="km")
route.add_location("Jaipur", "Udaipur", 394, unit="km")

calc = DistanceCalculator(person=person, route=route)
route_result = calc.calculate_route()

report_gen = ReportGenerator(route_result)
print(report_gen.generate_text())
```

### 4. Comprehensive Reports and Chart Visualizations

Export calculated route results into JSON, CSV, PDF, and Matplotlib graphs:

```python
from stepdistance import plot_all, ReportGenerator

report_gen = ReportGenerator(route_result)

# Export structured report files
report_gen.save_json("report.json")
report_gen.save_csv("report.csv")
report_gen.save_pdf("report.pdf")

# Plot Matplotlib graphs (Bar, Pie, Line)
chart_files = plot_all(route_result, save_dir="./charts")
for chart in chart_files:
    print(f"Generated chart: {chart}")
```

### 5. Custom Exceptions and Error Handling

Handle invalid distances, units, or step lengths cleanly:

```python
from stepdistance import Person, DistanceCalculator, StepDistanceError, InvalidDistanceError

person = Person(name="Test User", step_length=0.75)
calc = DistanceCalculator(person=person)

try:
    calc.calculate_steps(distance=-50, unit="km")
except InvalidDistanceError as e:
    print(f"Distance validation error: {e}")
except StepDistanceError as e:
    print(f"General step distance error: {e}")
```

---

## Command Line & Interactive Mode

### Interactive Menu Mode

Launch the interactive console application:

```bash
stepdistance interactive
```

```text
============================================================
      Welcome to StepDistanceCalculator Interactive Mode
============================================================

1. Calculate Single Distance
2. Add Segment to Current Route
3. View Current Route & Calculate Steps
4. Clear Current Route
5. Change Person Info
6. View Calculation History
7. Export Reports (JSON / CSV / PDF)
8. Generate Graph Visualizations
9. Exit
```

### CLI Subcommands

Calculate a single distance:

```bash
stepdistance calculate --from Delhi --to Agra --distance 233 --unit km --step-length 0.75
```

Calculate steps from a route JSON specification file:

```bash
stepdistance route --file route.json --output-dir ./output
```

---

## PyPI Publishing Guide

To build and publish this package to PyPI, use `build` and `twine`:

### 1. Install Publishing Tools

```bash
pip install build twine
```

### 2. Build Package Distributions

Generate source tarball and wheel distributions:

```bash
python -m build
```

This populates the `dist/` directory with `.tar.gz` and `.whl` files.

### 3. Verify Package Metadata

```bash
twine check dist/*
```

### 4. Upload to PyPI

Upload the package to PyPI:

```bash
twine upload dist/*
```

---

## Running Unit Tests

Run the full pytest suite:

```bash
pytest tests/ -v
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

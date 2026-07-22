# StepDistanceCalculator 🚶‍♂️📏

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/StepDistanceCalculator/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/StepDistanceCalculator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional, object-oriented Python package to calculate walking step counts between places or cities based on distance, unit conversion, pace activity modes, and biomechanically accurate step length estimation.

---

## 🌟 Key Features

- **Single & Multi-City Route Calculation**: Compute exact and rounded step counts for single legs or multi-segment route chains.
- **Biomechanical Step Estimation**:
  - **Height-Based Estimation**: Step length calculated from height (`Step Length = Height × Gender Factor`).
  - **Gender Defaults**: Default average step lengths (Adult Male: `0.78m`, Adult Female: `0.70m`, Neutral: `0.74m`).
  - **Stride Length Support**: Convert 2-step stride lengths to step length.
  - **Pace Adjustments**: Multipliers for Walking (`1.0x`), Brisk Walking (`1.08x`), Jogging (`1.25x`), Running (`1.40x`), and Hilly/Uphill (`0.90x`).
- **Automatic Unit Conversions**: Supports `meters` (`m`), `kilometers` (`km`), `miles`, and `feet` (`ft`).
- **Flexible Rounding Modes**: Choose between `ceil` (default), `round`, `floor`, and `exact`.
- **Rich Reports & Exporting**: Generate formatted **Text**, **JSON**, **CSV**, and **PDF** reports.
- **Data Visualizations**: Built-in Matplotlib chart generators:
  - 📊 **Bar Chart**: Steps per route segment
  - 🥧 **Pie Chart**: Distance percentage breakdown
  - 📈 **Line Chart**: Cumulative step counts across route checkpoints
- **Interactive Console & CLI**: Launch `stepdistance interactive` for a menu-driven terminal experience or use subcommand arguments.
- **Robust & Fully Tested**: 100% test coverage with `pytest`, input validation, and custom exceptions.

---

## 🚀 Quick Start & Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install StepDistanceCalculator
```

### Option 2: Install from Source / Local Development

```bash
# Clone repository
git clone https://github.com/Amit123103/Stepcount_python_module.git
cd Stepcount_python_module

# Install in editable mode
pip install -e .
```

---

## 💻 Python Usage Examples

### 1. Basic Single Distance Calculation

```python
from stepdistance import Person, DistanceCalculator

# Define person with custom step length
person = Person(name="Amit", step_length=0.75, pace="brisk_walking")
calc = DistanceCalculator(person=person)

# Calculate steps for 233 km (Delhi -> Agra)
result = calc.calculate_steps(distance=233, unit="km", origin="Delhi", destination="Agra")

print(f"Location       : {result.origin} -> {result.destination}")
print(f"Distance       : {result.distance_m:,.0f} m")
print(f"Effective SL   : {result.step_length:.4f} m")
print(f"Steps Required : {result.steps_rounded:,}")
# Output: Steps Required: 287,655
```

### 2. Height-Based Biomechanical Step Calculation

```python
from stepdistance import Person, DistanceCalculator

# Calculate step length from height (e.g. 175 cm male)
person = Person(name="Rahul", height=175, height_unit="cm", gender="male", pace="walking")
print(f"Calculated Step Length: {person.step_length:.4f} m")  # ~0.7263 m

calc = DistanceCalculator(person=person)
res = calc.calculate_steps(distance=5, unit="km", origin="Home", destination="Park")
print(f"Steps: {res.steps_rounded:,}")
```

### 3. Multi-City Route Chain & Reports

```python
from stepdistance import Person, Route, DistanceCalculator, ReportGenerator

person = Person(name="Amit", height=178, height_unit="cm", gender="male")

# Build a multi-segment route
route = Route()
route.add_location("Delhi", "Agra", 233, unit="km")
route.add_location("Agra", "Jaipur", 238, unit="km")
route.add_location("Jaipur", "Udaipur", 394, unit="km")

calc = DistanceCalculator(person=person, route=route)
route_result = calc.calculate_route()

# Generate plain text report
report_gen = ReportGenerator(route_result)
print(report_gen.generate_text())

# Export reports to JSON, CSV, and PDF
report_gen.save_json("reports/route_report.json")
report_gen.save_csv("reports/route_report.csv")
report_gen.save_pdf("reports/route_report.pdf")
```

### 4. Matplotlib Chart Visualizations

```python
from stepdistance import plot_all, plot_steps_bar, plot_distance_pie, plot_cumulative_line

# Generate all 3 charts and save to output directory
chart_paths = plot_all(route_result, save_dir="./charts")

for path in chart_paths:
    print(f"Saved chart: {path}")
```

---

## 🛠️ CLI & Interactive Console Mode

### Interactive Menu Mode

Launch the interactive console menu:

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

**Calculate single distance:**

```bash
stepdistance calculate --from Delhi --to Agra --distance 233 --unit km --height 175 --gender male --pace brisk_walking
```

**Calculate route from JSON file:**

```bash
stepdistance route --file examples/route.json --output-dir ./output
```

---

## 📁 Project Structure

```text
StepDistanceCalculator/
│
├── stepdistance/            # Core package
│   ├── __init__.py          # Main exports & API
│   ├── person.py            # Person model & biomechanical step estimation
│   ├── location.py          # Location data class
│   ├── route.py             # Route & Segment models
│   ├── calculator.py        # DistanceCalculator & result classes
│   ├── converter.py         # Unit conversion module (m, km, miles, ft, cm, in)
│   ├── reports.py           # ReportGenerator (Text, JSON, CSV, PDF)
│   ├── visualization.py     # Matplotlib charts (Bar, Pie, Line)
│   ├── utils.py             # Validation & logging helpers
│   └── cli.py               # CLI & Interactive Menu interface
│
├── examples/                # Usage script examples
│   ├── basic_usage.py
│   ├── multi_city.py
│   └── generate_reports.py
│
├── tests/                   # Pytest suite (39 test cases)
│   ├── test_calculator.py
│   ├── test_cli.py
│   ├── test_converter.py
│   ├── test_location.py
│   ├── test_person.py
│   ├── test_reports.py
│   ├── test_route.py
│   └── test_utils.py
│
├── .github/workflows/       # GitHub Actions automated PyPI publisher
│   └── publish.yml
│
├── pyproject.toml           # Build system config
├── setup.py                 # Setup configuration
├── requirements.txt         # Project dependencies
└── README.md
```

---

## 🧪 Running Unit Tests

Run the full pytest suite:

```bash
pytest tests/ -v
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

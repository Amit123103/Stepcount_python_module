# StepDistanceCalculator 🚶‍♂️📏

A professional, object-oriented Python package to calculate walking step counts between places or cities based on total distance, unit conversion, and average step lengths.

---

## 🌟 Features

- **Single & Multi-City Calculation**: Compute step counts for single routes or multi-segment route chains.
- **Default & Custom Step Lengths**: Default values based on gender (Adult Male: `0.78m`, Adult Female: `0.70m`) or custom length.
- **Automatic Unit Conversion**: Seamlessly convert distances in `meters`, `kilometers`, `miles`, and `feet` to meters.
- **Clean Object-Oriented Design**: Core domain abstractions including `Person`, `Location`, `Route`, `DistanceCalculator`, and `ReportGenerator`.
- **Comprehensive Reports**: Export reports as plain text, **JSON**, **CSV**, or formatted **PDF**.
- **Data Visualization**: Generate matplotlib charts for segment steps (bar chart), percentage distance contribution (pie chart), and cumulative steps (line chart).
- **CLI & Interactive Mode**: Built-in Command Line Interface with interactive menu mode.
- **Robust & Validated**: Input validation, custom exception hierarchy, and structured logging.

---

## 📁 Project Structure

```text
StepDistanceCalculator/
│
├── stepdistance/
│   ├── __init__.py          # Package exports & versioning
│   ├── person.py            # Person class (name, gender, step length)
│   ├── location.py          # Location data class
│   ├── route.py             # Route and Segment classes
│   ├── calculator.py        # DistanceCalculator & result dataclasses
│   ├── converter.py         # Unit conversion module
│   ├── reports.py           # ReportGenerator (Text, JSON, CSV, PDF)
│   ├── visualization.py     # Matplotlib charts (Bar, Pie, Line)
│   ├── utils.py             # Validators, logging & exceptions
│   └── cli.py               # CLI & Interactive Menu Program
│
├── examples/
│   ├── basic_usage.py       # Single distance calculation
│   ├── multi_city.py        # Multi-city route calculation
│   └── generate_reports.py  # Exporting JSON/CSV/PDF & Charts
│
├── tests/
│   ├── test_converter.py
│   ├── test_person.py
│   ├── test_location.py
│   ├── test_route.py
│   ├── test_calculator.py
│   ├── test_reports.py
│   └── test_utils.py
│
├── docs/
│   └── usage_guide.md
├── pyproject.toml
├── setup.py
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Installation

Install locally in editable mode:

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

---

## 💻 Python Usage Examples

### 1. Basic Single Calculation

```python
from stepdistance import Person, DistanceCalculator

person = Person(name="Amit", step_length=0.75)
calc = DistanceCalculator(person=person)

result = calc.calculate_steps(distance=233, unit="km", origin="Delhi", destination="Agra")

print(f"Steps required: {result.steps_rounded:,}")
# Output: Steps required: 310,667
```

### 2. Multi-City Route Chain

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

### 3. Generate Reports & Charts

```python
# Export reports
report_gen.save_json("report.json")
report_gen.save_csv("report.csv")
report_gen.save_pdf("report.pdf")

# Plot matplotlib graphs
from stepdistance import plot_all
plot_all(route_result, save_dir="./charts")
```

---

## 🛠️ Command Line & Interactive Mode

Launch the interactive menu-driven program:

```bash
stepdistance interactive
```

Calculate via command line arguments:

```bash
stepdistance calculate --from Delhi --to Agra --distance 233 --unit km --step-length 0.75
```

---

## 🧪 Running Unit Tests

Run the test suite with `pytest`:

```bash
pytest tests/ -v
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).


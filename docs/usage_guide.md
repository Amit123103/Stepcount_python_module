# StepDistanceCalculator User Guide

## Overview
`StepDistanceCalculator` is a feature-packed Python package designed to estimate the number of walking steps required to traverse distances between cities or locations.

---

## Key Formulas

$$\text{Steps} = \frac{\text{Distance in Meters}}{\text{Step Length in Meters}}$$

### Default Step Lengths
- **Adult Male**: $0.78 \text{ m}$
- **Adult Female**: $0.70 \text{ m}$
- **Neutral Default**: $0.74 \text{ m}$

---

## Unit Conversions

| Unit | Factor to Meters | Function |
|---|---|---|
| Metres (`m`) | $1.0$ | Direct |
| Kilometres (`km`) | $1,000.0$ | `km_to_meters()` |
| Miles (`miles`) | $1,609.344$ | `miles_to_meters()` |
| Feet (`feet`) | $0.3048$ | `feet_to_meters()` |

---

## Exporting Reports & Graphs

The package provides `ReportGenerator` to save reports in multiple formats:
- **Text**: `rg.generate_text()`
- **JSON**: `rg.save_json("report.json")`
- **CSV**: `rg.save_csv("report.csv")`
- **PDF**: `rg.save_pdf("report.pdf")`

Visualization options include:
- `plot_steps_bar()`: Bar chart showing steps per segment.
- `plot_distance_pie()`: Pie chart showing distance percentages.
- `plot_cumulative_line()`: Line chart showing step progression.
- `plot_all()`: Generates all three charts in one call.

"""
Example 3: Exporting Reports & Matplotlib Charts
Demonstrates exporting reports to JSON, CSV, PDF and generating graphs.
"""

import os
from stepdistance import DistanceCalculator, Person, ReportGenerator, Route, plot_all


def main():
    print("--- Report & Visualization Export Example ---")

    # 1. Setup Person & Route
    person = Person(name="Amit", gender="male")  # Uses default 0.78m
    route = Route()
    route.add_from_tuples(
        [
            ("Delhi", "Agra", 233),
            ("Agra", "Jaipur", 238),
            ("Jaipur", "Udaipur", 394),
        ],
        unit="km",
    )

    # 2. Perform Calculation
    calc = DistanceCalculator(person=person, route=route)
    result = calc.calculate_route()

    # 3. Export Reports
    output_dir = "./output_demo"
    os.makedirs(output_dir, exist_ok=True)

    rg = ReportGenerator(result)
    json_file = rg.save_json(f"{output_dir}/route_report.json")
    csv_file = rg.save_csv(f"{output_dir}/route_report.csv")
    pdf_file = rg.save_pdf(f"{output_dir}/route_report.pdf")

    print(f"JSON Report saved to : {json_file}")
    print(f"CSV Report saved to  : {csv_file}")
    print(f"PDF Report saved to  : {pdf_file}")

    # 4. Generate Visualization Charts
    chart_paths = plot_all(result, save_dir=f"{output_dir}/charts")
    print("\nGenerated Charts:")
    for path in chart_paths:
        print(f" - {path}")


if __name__ == "__main__":
    main()

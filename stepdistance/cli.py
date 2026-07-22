"""
stepdistance.cli
================

Command Line Interface (CLI) and interactive menu-driven interface.

Provides:
    - Subcommands for single distance calculations and multi-city route files.
    - Height-based step length estimation, pace selection, and rounding mode controls.
    - An interactive menu-driven console program.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from stepdistance.calculator import DistanceCalculator
from stepdistance.person import Person
from stepdistance.reports import ReportGenerator
from stepdistance.route import Route
from stepdistance.utils import setup_logging
from stepdistance.visualization import plot_all


def _prompt_person() -> Person:
    """Prompt user interactively for Person information."""
    print("\n--- Person Information ---")
    name = input("Enter Person Name [Default: Amit]: ").strip() or "Amit"

    print("\nSelect Step Length determination method:")
    print("  1. Adult Male Default (0.78 m)")
    print("  2. Adult Female Default (0.70 m)")
    print("  3. Calculate from Height (Biomechanically Accurate)")
    print("  4. Custom Step Length (meters)")
    print("  5. Stride Length (meters)")
    print("  6. Neutral Default (0.74 m)")

    choice = input("Enter choice (1-6) [Default: 3]: ").strip() or "3"

    # Select Pace mode
    print("\nSelect Pace Mode:")
    print("  1. Walking (1.0x)")
    print("  2. Brisk Walking (1.08x)")
    print("  3. Jogging (1.25x)")
    print("  4. Running (1.40x)")
    print("  5. Hilly / Uphill (0.90x)")
    pace_choice = input("Enter pace choice (1-5) [Default: 1]: ").strip() or "1"
    pace_map = {
        "1": "walking",
        "2": "brisk_walking",
        "3": "jogging",
        "4": "running",
        "5": "hilly",
    }
    pace = pace_map.get(pace_choice, "walking")

    if choice == "1":
        return Person(name=name, gender="male", pace=pace)
    elif choice == "2":
        return Person(name=name, gender="female", pace=pace)
    elif choice == "3":
        while True:
            try:
                h_str = input("Enter height in cm (e.g. 175): ").strip()
                h = float(h_str)
                g_str = input("Gender (male / female / neutral) [Default: neutral]: ").strip().lower() or None
                return Person(name=name, height=h, height_unit="cm", gender=g_str, pace=pace)
            except ValueError as e:
                print(f"Invalid height input: {e}. Please enter a positive number.")
    elif choice == "4":
        while True:
            try:
                sl_str = input("Enter step length in meters (e.g. 0.75): ").strip()
                sl = float(sl_str)
                return Person(name=name, step_length=sl, pace=pace)
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a positive number.")
    elif choice == "5":
        while True:
            try:
                stride_str = input("Enter full stride length in meters (e.g. 1.50): ").strip()
                stride = float(stride_str)
                return Person(name=name, stride_length=stride, pace=pace)
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a positive number.")
    else:
        return Person(name=name, pace=pace)


def interactive_menu() -> None:
    """Run an interactive menu-driven program for StepDistanceCalculator."""
    print("=" * 60)
    print("      Welcome to StepDistanceCalculator Interactive Mode")
    print("=" * 60)

    person = _prompt_person()
    print(f"\nActive Person: {person}")

    route = Route()
    calc = DistanceCalculator(person=person, route=route)

    while True:
        print("\n" + "=" * 40)
        print("                MAIN MENU")
        print("=" * 40)
        print("1. Calculate Single Distance")
        print("2. Add Segment to Current Route")
        print("3. View Current Route & Calculate Steps")
        print("4. Clear Current Route")
        print("5. Change Person Info")
        print("6. View Calculation History")
        print("7. Export Reports (JSON / CSV / PDF)")
        print("8. Generate Graph Visualizations")
        print("9. Exit")
        print("=" * 40)

        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            print("\n--- Single Distance Calculation ---")
            origin = input("Starting Place Name [e.g. Home]: ").strip() or "Home"
            dest = input("Destination Place Name [e.g. Park]: ").strip() or "Park"
            dist_str = input("Distance [e.g. 5]: ").strip()
            unit = input("Unit (m, km, miles, feet) [Default: km]: ").strip() or "km"

            try:
                dist = float(dist_str)
                res = calc.calculate_steps(dist, unit=unit, origin=origin, destination=dest)
                print("\n" + "-" * 40)
                print(f"{res.origin} → {res.destination}")
                print(f"Distance       : {dist} {unit} ({res.distance_m:,.2f} m)")
                print(f"Effective SL   : {res.step_length:.4f} m (Pace: {res.pace})")
                print(f"Steps Required : {res.steps_rounded:,} (Exact: {res.steps_exact:,.2f})")
                print("-" * 40)
            except Exception as e:
                print(f"Error calculating steps: {e}")

        elif choice == "2":
            print("\n--- Add Route Segment ---")
            origin = input("Origin City/Place: ").strip()
            dest = input("Destination City/Place: ").strip()
            dist_str = input("Distance: ").strip()
            unit = input("Unit (m, km, miles, feet) [Default: km]: ").strip() or "km"

            try:
                dist = float(dist_str)
                route.add_segment(origin, dest, dist, unit=unit)
                print(f"Segment '{origin} → {dest}' ({dist} {unit}) added.")
            except Exception as e:
                print(f"Error adding segment: {e}")

        elif choice == "3":
            if route.segment_count == 0:
                print("\nCurrent route is empty! Add segments first.")
            else:
                try:
                    res = calc.calculate_route(route)
                    report = ReportGenerator(res)
                    print("\n" + report.generate_text())
                except Exception as e:
                    print(f"Error calculating route: {e}")

        elif choice == "4":
            route = Route()
            calc.route = route
            print("\nCurrent route cleared.")

        elif choice == "5":
            person = _prompt_person()
            calc.person = person
            print(f"\nUpdated Person: {person}")

        elif choice == "6":
            history = calc.get_history()
            if not history:
                print("\nNo history recorded yet.")
            else:
                print("\n--- Calculation History ---")
                for entry in history:
                    print(
                        f"[{entry.timestamp}] {entry.person_name} | "
                        f"{entry.origin} → {entry.destination} : "
                        f"{entry.distance_m:,.0f} m -> {entry.steps:,} steps"
                    )

        elif choice == "7":
            if route.segment_count == 0:
                print("\nCurrent route is empty! Build a route first before exporting.")
            else:
                try:
                    res = calc.calculate_route(route)
                    rg = ReportGenerator(res)

                    out_dir = input("Enter output directory [Default: ./reports]: ").strip() or "./reports"
                    fmt = input("Export format (json, csv, pdf, all) [Default: all]: ").strip().lower() or "all"

                    if fmt in ("json", "all"):
                        p = rg.save_json(f"{out_dir}/report.json")
                        print(f"Saved JSON: {p}")
                    if fmt in ("csv", "all"):
                        p = rg.save_csv(f"{out_dir}/report.csv")
                        print(f"Saved CSV: {p}")
                    if fmt in ("pdf", "all"):
                        p = rg.save_pdf(f"{out_dir}/report.pdf")
                        print(f"Saved PDF: {p}")

                except Exception as e:
                    print(f"Error exporting reports: {e}")

        elif choice == "8":
            if route.segment_count == 0:
                print("\nCurrent route is empty! Build a route first before generating charts.")
            else:
                try:
                    res = calc.calculate_route(route)
                    out_dir = input("Enter output directory for charts [Default: ./charts]: ").strip() or "./charts"
                    paths = plot_all(res, save_dir=out_dir)
                    print("\nCharts generated successfully:")
                    for path in paths:
                        print(f" - {path}")
                except Exception as e:
                    print(f"Error generating charts: {e}")

        elif choice == "9":
            print("\nThank you for using StepDistanceCalculator!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter a number from 1 to 9.")


def main() -> None:
    """Main CLI entry point."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="StepDistanceCalculator: Calculate walking step counts for routes."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Interactive sub-command
    subparsers.add_parser("interactive", help="Run menu-driven interactive mode")

    # Single calculation sub-command
    single_parser = subparsers.add_parser("calculate", help="Calculate steps for a single distance")
    single_parser.add_argument("--from", dest="origin", default="Origin", help="Starting place name")
    single_parser.add_argument("--to", dest="destination", default="Destination", help="Destination place name")
    single_parser.add_argument("--distance", "-d", type=float, required=True, help="Distance value")
    single_parser.add_argument("--unit", "-u", default="km", choices=["m", "km", "miles", "feet"], help="Distance unit")
    single_parser.add_argument("--person", default="Walker", help="Person name")
    single_parser.add_argument("--step-length", type=float, help="Step length in meters")
    single_parser.add_argument("--stride-length", type=float, help="Full stride length in meters (2 steps)")
    single_parser.add_argument("--height", type=float, help="Person height value")
    single_parser.add_argument("--height-unit", default="cm", choices=["cm", "m", "in", "feet", "ft"], help="Height unit")
    single_parser.add_argument("--gender", choices=["male", "female"], help="Person gender")
    single_parser.add_argument(
        "--pace",
        default="walking",
        choices=["walking", "brisk_walking", "jogging", "running", "hilly"],
        help="Activity pace mode",
    )
    single_parser.add_argument(
        "--rounding-mode",
        default="ceil",
        choices=["ceil", "round", "floor", "exact"],
        help="Step rounding mode",
    )

    # Route JSON file sub-command
    route_parser = subparsers.add_parser("route", help="Calculate steps for a route JSON file")
    route_parser.add_argument("--file", "-f", required=True, help="Path to JSON file containing route segments")
    route_parser.add_argument("--person", default="Walker", help="Person name")
    route_parser.add_argument("--step-length", type=float, help="Step length in meters")
    route_parser.add_argument("--stride-length", type=float, help="Full stride length in meters")
    route_parser.add_argument("--height", type=float, help="Person height value")
    route_parser.add_argument("--height-unit", default="cm", choices=["cm", "m", "in", "feet", "ft"], help="Height unit")
    route_parser.add_argument("--gender", choices=["male", "female"], help="Person gender")
    route_parser.add_argument(
        "--pace",
        default="walking",
        choices=["walking", "brisk_walking", "jogging", "running", "hilly"],
        help="Activity pace mode",
    )
    route_parser.add_argument(
        "--rounding-mode",
        default="ceil",
        choices=["ceil", "round", "floor", "exact"],
        help="Step rounding mode",
    )
    route_parser.add_argument("--output-dir", "-o", help="Directory to save JSON/CSV/PDF and charts")

    args = parser.parse_args()

    if args.command == "interactive" or args.command is None:
        interactive_menu()
        return

    person = Person(
        name=args.person,
        step_length=args.step_length,
        stride_length=getattr(args, "stride_length", None),
        height=getattr(args, "height", None),
        height_unit=getattr(args, "height_unit", "cm"),
        gender=getattr(args, "gender", None),
        pace=getattr(args, "pace", "walking"),
    )

    if args.command == "calculate":
        calc = DistanceCalculator(person)
        res = calc.calculate_steps(
            distance=args.distance,
            unit=args.unit,
            origin=args.origin,
            destination=args.destination,
            pace=person.pace,
            rounding_mode=getattr(args, "rounding_mode", "ceil"),
        )
        print("=" * 50)
        print(f"Person: {person.name} (Effective SL: {res.step_length:.4f} m/step, Pace: {res.pace})")
        print(f"Segment: {res.origin} -> {res.destination}")
        print(f"Distance: {args.distance} {args.unit} ({res.distance_m:,.2f} m)")
        print(f"Steps Required: {res.steps_rounded:,} (Exact: {res.steps_exact:,.2f})")
        print("=" * 50)

    elif args.command == "route":
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)

        route = Route()
        for seg in data.get("segments", []):
            route.add_segment(
                origin=seg["origin"],
                destination=seg["destination"],
                distance=float(seg["distance"]),
                unit=seg.get("unit", "km"),
            )

        calc = DistanceCalculator(person=person, route=route)
        res = calc.calculate_route(
            pace=person.pace,
            rounding_mode=getattr(args, "rounding_mode", "ceil"),
        )
        rg = ReportGenerator(res)
        print(rg.generate_text())

        if args.output_dir:
            rg.save_json(f"{args.output_dir}/report.json")
            rg.save_csv(f"{args.output_dir}/report.csv")
            rg.save_pdf(f"{args.output_dir}/report.pdf")
            plot_all(res, save_dir=f"{args.output_dir}/charts")
            print(f"\nExported reports and charts to: {args.output_dir}")


if __name__ == "__main__":
    main()

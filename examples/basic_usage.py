"""
Example 1: Basic Usage
Demonstrates single distance calculation with Person and DistanceCalculator.
"""

from stepdistance import DistanceCalculator, Person, km_to_meters


def main():
    print("--- Single Distance Calculation Example ---")

    # 1. Create a Person
    person = Person(name="Amit", step_length=0.75)
    print(person.summary())

    # 2. Initialize Calculator
    calc = DistanceCalculator(person=person)

    # 3. Calculate steps for a single segment (e.g., Delhi to Agra: 233 km)
    distance_km = 233
    result = calc.calculate_steps(
        distance=distance_km,
        unit="km",
        origin="Delhi",
        destination="Agra",
    )

    print("\nResult:")
    print(f"Route           : {result.origin} -> {result.destination}")
    print(f"Distance        : {distance_km} km ({result.distance_m:,.0f} m)")
    print(f"Exact Steps     : {result.steps_exact:,.2f}")
    print(f"Rounded Steps   : {result.steps_rounded:,}")

    # 4. Demonstrate converter helper
    meters = km_to_meters(233)
    print(f"\nDirect Conversion Check: 233 km = {meters:,.2f} meters")


if __name__ == "__main__":
    main()

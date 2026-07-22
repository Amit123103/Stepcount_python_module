"""
Example 2: Multi-City Route Chain Calculator
Demonstrates route chaining with Delhi -> Agra -> Jaipur -> Udaipur.
"""

from stepdistance import DistanceCalculator, Person, ReportGenerator, Route


def main():
    print("--- Multi-City Route Chain Example ---")

    # 1. Create a Person
    person = Person(name="Amit", step_length=0.75)

    # 2. Build a Route
    route = Route()
    route.add_location("Delhi", "Agra", 233, unit="km")
    route.add_location("Agra", "Jaipur", 238, unit="km")
    route.add_location("Jaipur", "Udaipur", 394, unit="km")

    # 3. Calculate steps for the entire route
    calc = DistanceCalculator(person=person, route=route)
    route_result = calc.calculate_route()

    # 4. Generate formatted text report
    report_gen = ReportGenerator(route_result)
    print(report_gen.generate_text())


if __name__ == "__main__":
    main()

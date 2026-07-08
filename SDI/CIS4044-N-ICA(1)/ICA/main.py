# Main entry point for the historical weather application.
#
# Run it from inside the ICA folder:
#   python3 main.py          -> interactive menu
#   python3 main.py demo     -> run every phase 1 query and create all charts
#   python3 main.py charts   -> create all charts only

import sys

from phase_1 import (
    connect_database,
    select_all_countries,
    select_all_cities,
    average_annual_temperature,
    average_seven_day_precipitation,
    average_mean_temp_by_city,
    average_annual_precipitation_by_country,
    monthly_temperature_summary,
    wettest_city_by_year,
)
from phase_2 import generate_all_charts
from phase_3 import update_city_weather


def run_demo(connection):
    # Run every phase 1 query with example values, then create the charts.
    # No network is needed, so this always works offline.
    print("\nPhase 1: countries")
    select_all_countries(connection)
    print("\nPhase 1: cities")
    select_all_cities(connection)
    print("\nPhase 1: annual temperature")
    average_annual_temperature(connection, city_id=1, year=2024)
    print("\nPhase 1: seven-day precipitation")
    average_seven_day_precipitation(connection, city_id=1, start_date="2024-01-01")
    print("\nPhase 1: average mean temperature by city")
    average_mean_temp_by_city(connection, date_from="2024-01-01", date_to="2024-12-31")
    print("\nPhase 1: country precipitation")
    average_annual_precipitation_by_country(connection, year=2024)
    print("\nPhase 1: extra monthly summary")
    monthly_temperature_summary(connection, city_id=1, year=2024)
    print("\nPhase 1: extra wettest city ranking")
    wettest_city_by_year(connection)
    print("\nPhase 2: sample charts")
    generate_all_charts(connection)


def run_menu(connection):
    # A simple text menu, so each part can be shown one at a time.
    while True:
        print()
        print("Historical Weather Data")
        print("1. List countries")
        print("2. List cities")
        print("3. Average annual temperature")
        print("4. Average seven-day precipitation")
        print("5. Generate all charts")
        print("6. Update city weather from Open-Meteo")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                select_all_countries(connection)
            elif choice == "2":
                select_all_cities(connection)
            elif choice == "3":
                city_id = int(input("City id: "))
                year = int(input("Year: "))
                average_annual_temperature(connection, city_id, year)
            elif choice == "4":
                city_id = int(input("City id: "))
                start_date = input("Start date (YYYY-MM-DD): ").strip()
                average_seven_day_precipitation(connection, city_id, start_date)
            elif choice == "5":
                generate_all_charts(connection)
            elif choice == "6":
                city_id = int(input("City id: "))
                start_date = input("Start date (YYYY-MM-DD): ").strip()
                end_date = input("End date (YYYY-MM-DD): ").strip()
                update_city_weather(connection, city_id, start_date, end_date)
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
        except Exception as error:
            # Show the problem and go back to the menu instead of crashing.
            print("Error:", error)


if __name__ == "__main__":
    connection = connect_database()
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo(connection)
    elif len(sys.argv) > 1 and sys.argv[1] == "charts":
        generate_all_charts(connection)
    else:
        run_menu(connection)
    connection.close()

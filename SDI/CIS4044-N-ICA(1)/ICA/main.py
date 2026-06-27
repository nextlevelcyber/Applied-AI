"""Single entry point for the historical weather ICA application."""

from __future__ import annotations

import argparse
import sys

try:
    from .common import DEFAULT_DB_PATH, connect_database
    from .phase_1 import (
        average_annual_precipitation_by_country,
        average_annual_temperature,
        average_mean_temp_by_city,
        average_seven_day_precipitation,
        monthly_temperature_summary,
        select_all_cities,
        select_all_countries,
        wettest_city_by_year,
    )
    from .phase_2 import generate_all_sample_charts
    from .phase_3 import update_city_weather
except ImportError:
    from common import DEFAULT_DB_PATH, connect_database  # type: ignore
    from phase_1 import (  # type: ignore
        average_annual_precipitation_by_country,
        average_annual_temperature,
        average_mean_temp_by_city,
        average_seven_day_precipitation,
        monthly_temperature_summary,
        select_all_cities,
        select_all_countries,
        wettest_city_by_year,
    )
    from phase_2 import generate_all_sample_charts  # type: ignore
    from phase_3 import update_city_weather  # type: ignore


def run_demo(db_path=DEFAULT_DB_PATH) -> None:
    """Run a deterministic demonstration that does not call the network."""

    with connect_database(db_path) as connection:
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
        generate_all_sample_charts(connection)


def run_menu(db_path=DEFAULT_DB_PATH) -> None:
    """Small interactive menu for manual demonstration."""

    actions = {
        "1": ("List countries", lambda conn: select_all_countries(conn)),
        "2": ("List cities", lambda conn: select_all_cities(conn)),
        "3": ("Average annual temperature", _menu_average_temperature),
        "4": ("Average seven-day precipitation", _menu_average_precipitation),
        "5": ("Generate sample charts", lambda conn: generate_all_sample_charts(conn)),
        "6": ("Update city weather from Open-Meteo", _menu_update_weather),
        "0": ("Exit", None),
    }

    with connect_database(db_path) as connection:
        while True:
            print("\nHistorical Weather Data")
            for key, (label, _) in actions.items():
                print(f"{key}. {label}")
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye.")
                return
            action = actions.get(choice)
            if action is None:
                print("Invalid option.")
                continue
            try:
                action[1](connection)
            except (ValueError, RuntimeError) as exc:
                print(f"Error: {exc}")


def _menu_average_temperature(connection) -> None:
    city_id = int(input("City id: ").strip())
    year = int(input("Year: ").strip())
    average_annual_temperature(connection, city_id, year)


def _menu_average_precipitation(connection) -> None:
    city_id = int(input("City id: ").strip())
    start_date = input("Start date (YYYY-MM-DD): ").strip()
    average_seven_day_precipitation(connection, city_id, start_date)


def _menu_update_weather(connection) -> None:
    city_id = int(input("City id: ").strip())
    start_date = input("Start date (YYYY-MM-DD): ").strip()
    end_date = input("End date (YYYY-MM-DD): ").strip()
    update_city_weather(connection, city_id, start_date, end_date)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Historical weather ICA application")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Path to the SQLite database")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("demo", help="Run deterministic Phase 1 and Phase 2 demonstration")
    subparsers.add_parser("menu", help="Run the interactive console menu")
    subparsers.add_parser("charts", help="Generate all sample charts")

    update_parser = subparsers.add_parser("update-weather", help="Fetch and store Open-Meteo data")
    update_parser.add_argument("city_id", type=int)
    update_parser.add_argument("start_date")
    update_parser.add_argument("end_date")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "demo"

    if command == "demo":
        run_demo(args.db)
    elif command == "menu":
        run_menu(args.db)
    elif command == "charts":
        with connect_database(args.db) as connection:
            generate_all_sample_charts(connection)
    elif command == "update-weather":
        with connect_database(args.db) as connection:
            update_city_weather(connection, args.city_id, args.start_date, args.end_date)
    else:
        parser.error(f"Unknown command: {command}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


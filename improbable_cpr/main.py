import argparse
import itertools
import re
from datetime import date
from typing import Any
from typing import Callable

from improbable_cpr.cpr_builder import CprBuilder
from improbable_cpr.generators import Gender


number_list_regex = r"(\d+)(,|$)|(\d+)-(\d+)"


def main_cli() -> CprBuilder:
    argument_parser = argparse.ArgumentParser(
        description="Generate CPR numbers suitible for testing. A CPR number is the national identity number of Denmark. This program generates CPR numbers that are suitible for testing, as they do not satisfy the modulo 11 test. These numbers are only allocated as a last resort.",
    )
    argument_parser.add_argument(
        "--year",
        type=str,
        help=f"List of years for which to generate CPR numbers. Should be on the format: {number_list_regex}",
    )
    argument_parser.add_argument(
        "--month",
        type=str,
        help=f"List of months for which to generate CPR numbers. Supports number representation for the months i.e. for January use '1'. Should be on the format: {number_list_regex}",
    )
    argument_parser.add_argument(
        "--day",
        type=str,
        help=f"List of days for which to generate CPR numbers. Should be on the format: {number_list_regex}",
    )
    argument_parser.add_argument(
        "--gender", type=Gender, choices=list(Gender), nargs="+"
    )
    argument_parser.add_argument(
        "--min_date",
        type=date.fromisoformat,
        help="The minimum date from which CPR numbers can be generated",
    )
    argument_parser.add_argument(
        "--max_date",
        type=date.fromisoformat,
        help="The maximum date from which CPR numbers can be generated",
    )
    argument_parser.add_argument(
        "--age",
        type=int,
        help="Generate CPR numbers for persons of a certain age",
    )
    argument_parser.add_argument(
        "--count", "-n", type=int, help="The number of CPR numbers to generate"
    )
    argument_parser.add_argument(
        "--format",
        type=str,
        choices=["dash", "no-dash"],
        help="Dash format (default) prints the CPR numbers with a dash before the running number",
        default="dash",
    )
    parsed_args = argument_parser.parse_args()
    builder = CprBuilder()

    if parsed_args.year is not None:
        list_parser(
            parsed_args.year, builder.with_year, builder.with_year_range
        )

    if parsed_args.month is not None:
        list_parser(
            parsed_args.month, builder.with_month, builder.with_month_range
        )

    if parsed_args.day is not None:
        list_parser(parsed_args.day, builder.with_day, builder.with_day_range)

    if parsed_args.gender is not None:
        builder.with_genders(parsed_args.gender)

    if parsed_args.min_date is not None:
        builder.with_min_date(parsed_args.min_date)

    if parsed_args.max_date is not None:
        builder.with_max_date(parsed_args.max_date)

    if parsed_args.age is not None:
        builder.with_age(parsed_args.age)

    cpr_iter = iter(builder)

    if parsed_args.count is not None:
        cpr_iter = itertools.islice(cpr_iter, parsed_args.count)

    for cpr in cpr_iter:
        if parsed_args.format == "dash":
            print(cpr.get_dash())
        else:
            print(cpr.get_no_dash())

    return builder


def list_parser(
    argument: str,
    single_func: Callable[[int], Any],
    range_func: Callable[[int, int], Any],
) -> None:
    for match in re.finditer(number_list_regex, argument):
        if match.group(1) is not None:
            single_func(int(match.group(1)))
        else:
            range_func(int(match.group(3)), int(match.group(4)))


if __name__ == "__main__":
    main_cli()

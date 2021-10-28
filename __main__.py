from argparse import ArgumentParser, Namespace
from datetime import datetime

from dateutil.relativedelta import relativedelta

from argument_validation import validate_day, validate_month, validate_year
from lech import Lech


def parse_args() -> Namespace:
    parser = ArgumentParser(description='Lech')
    parser.add_argument('day', type=validate_day, help='Birthday day')
    parser.add_argument('month', type=validate_month, help='Birthday month')
    parser.add_argument('year', type=validate_year, help='Birthday year')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    day = int(args.day)
    month = int(args.month)
    year = int(args.year)
    birthday = datetime(year, month, day)
    if relativedelta(datetime.now(), birthday).years < 18:
        exit('Not old enough')
    lech = Lech()
    lech.accept_cookies()
    lech.age_verification(day=day, month=month, year=year)
    lech.play()

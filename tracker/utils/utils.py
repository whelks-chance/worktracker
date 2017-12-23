from datetime import datetime
import holidays as holidays
import pytz
from govuk_bank_holidays.bank_holidays import BankHolidays


def get_holidays():
    dates = []
    for date, name in sorted(holidays.UnitedKingdom().items()):
        dates.append(date)
    return dates


def get_bank_holidays():

    # TODO sloooooow
    bank_holiday_dates = []
    bank_holidays = BankHolidays()

    # Hacky mess to convert dates to datetimes, localised to utc
    for bank_holiday in bank_holidays.get_holidays():
        # print(bank_holiday['title'], '>', bank_holiday['date'])
        bank_holiday_dates.append(
            pytz.utc.localize(
                datetime(bank_holiday['date'].year,
                         bank_holiday['date'].month,
                         bank_holiday['date'].day)
            )
        )

    return bank_holiday_dates

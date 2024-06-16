#!/usr/bin/env python3

"""Contains functions that are useful when building parameters, filters, and constraints.

As the optimization routine takes explicit values for filters, constraints,
parameters, and cost function, the functions in this module makes it easier to
create programatically an acceptable set of values based on arbitrary
constraints.

"""

from datetime import date, timedelta, datetime
from typing import List



def date_range(anchor_date: date, flex: int) -> List[date]:
  """Utility function. Allows for easy creation of date ranges for the optimization routine.

  The date_range allows to create a date-by-date range according to boundaries
  (ٍ± n days, called the `flex` parameter).

  """
  if flex <= 0:
    raise ValueError(
        "The flex parameter when creating a date range must be a positive integer."
    )
  return [anchor_date + timedelta(days=i) for i in range(-flex, flex + 1)]

def create_date_range(base_date, days):
  """
  Creates an array of dates from a base date.

  :param base_date: The base date as a string in the format 'YYYY-MM-DD'
  :param days: The number of days to add (positive) or subtract (negative)
  :return: A list of dates in the range
  """
  base_date_dt = datetime.strptime(base_date, '%Y-%m-%d')  # Convert string to datetime
  date_list = []

  if days >= 0:
    for i in range(days + 1):  # +1 to include the base_date itself
      date_list.append(base_date_dt + timedelta(days=i))
  else:
    for i in range(abs(days) + 1):  # +1 to include the base_date itself
      date_list.append(base_date_dt - timedelta(days=i))

  date_list.sort()
  # Format the dates for output
  formatted_date_list = [date.strftime('%Y-%m-%d') for date in date_list]

  return formatted_date_list

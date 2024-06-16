#!/usr/bin/env python3

"""Test cases for the utility functions used in the creation of the optimization
scenarios."""

# pylint: disable=wildcard-import, missing-function-docstring,
# pylint: disable=redefined-outer-name, unused-wildcard-import
# pylint: disable=bad-indentation

import random
from datetime import date
import pytest
from what_if.param_utils import date_range
from what_if.param_utils import create_date_range


def test_small_flex():
  """
    This test function verifies the behavior of the 'date_range' 
    function when the flex parameter is small. 
    It checks if the function returns a list of dates including the 
    specified date and the surrounding dates within the range of the given flex parameter.
    """
  base_date = date(2024, 2, 1)
  flex = 1
  expected_output = [date(2024, 1, 31), date(2024, 2, 1), date(2024, 2, 2)]

  result = date_range(base_date, flex)

  assert result == expected_output


def test_range_should_always_be_2n_plus_1():
  """
    This test function iterates over a range of values for 'n' 
    (randomly selected between 1 and 1,000) and verifies 
    that the length of the date range returned by the 'date_range' 
    function is always equal to 2*n + 1.
    """
  for _ in range(10):
      n = random.randrange(1, 1_000)
      base_date = date(2024, 2, 1)
      expected_length = 2 * n + 1

      result = date_range(base_date, n)

      assert len(result) == expected_length


def test_negative_flex_param_raise_value_error():
  """
    This test function checks if the 'date_range' function raises a ValueError 
    when a negative flex parameter is provided.
    """
  base_date = date(2024, 2, 1)
  flex = -1

  with pytest.raises(ValueError) as exc_info:
      _ = date_range(base_date, flex)

  assert exc_info.type is ValueError
  assert exc_info.value.args[0] == "The flex parameter when creating a date range must be a positive integer."


def test_positive_days():
    """
    This test function verifies the behavior of the 'create_date_range' function 
    when a positive number of days is provided.
    It checks if the function returns a list of dates starting from the base date 
    and extending for the specified number of days.
    """
    base_date = '2024-01-01'
    days = 5
    expected_dates = ['2024-01-01','2024-01-02','2024-01-03','2024-01-04','2024-01-05','2024-01-06']

    result = create_date_range(base_date, days)

    assert result == expected_dates

def test_negative_days():
    """
    This test function verifies the behavior of the 'create_date_range' 
    function when a negative number of days is provided.
    It checks if the function returns a list of dates starting from the base date 
    and going back for the absolute value of the specified number of days.
    """
    base_date = '2024-01-06'
    days = -5
    expected_dates = ['2024-01-01','2024-01-02','2024-01-03','2024-01-04','2024-01-05','2024-01-06']

    result = create_date_range(base_date, days)

    assert result == expected_dates

def test_zero_days():
    """
    This test function verifies the behavior of the 'create_date_range' function 
    when zero days are provided.
    It checks if the function returns a list containing only the base date.
    """
    base_date = '2024-01-01'
    days = 0
    expected_dates = ['2024-01-01']

    result = create_date_range(base_date, days)

    assert result == expected_dates

"""Test cases for the scenarios used by the general brute force approach. """

# pylint: disable=wildcard-import, missing-function-docstring,
# pylint: disable=redefined-outer-name, unused-wildcard-import
# pylint: disable=bad-indentation


import json

import pandas as pd
import pytest

from what_if.brute_force_general import optimize
from what_if.tne.json_utils import read_json_filters
from what_if.param_utils import create_date_range


def apply_filters(file_path):
  """Applies constrains from a JSON-formatted filters."""
  # Read filters from JSON file
  filters_json = read_json_filters(file_path)

  # Extract dates and flex_days from JSON filters
  base_date_from = filters_json["date_from"][0]
  base_date_to = filters_json["date_to"][0]
  flex_days = filters_json["flex_days"]

  # Calculate date ranges
  applied_filters = {
    "date_from": create_date_range(base_date_from, -flex_days),
    "date_to": create_date_range(base_date_to, flex_days),
  }
  return applied_filters


@pytest.fixture
def json_input_path(request):
  return request.param


@pytest.mark.parametrize(
  "json_input_path, expected_total_cost",
  [
    ("./scenarios/scenario1.json", 8464),
    ("./scenarios/scenario2.json", 5060),
    ("./scenarios/scenario3.json", 14304),
    ("./scenarios/scenario4.json", 9008),
    ("./scenarios/scenario5.json", 4338),
    ("./scenarios/scenario6.json", 14140),
    ("./scenarios/scenario7.json", 3486),
  ],
)

def test_scenario(json_input_path, expected_total_cost):
  with open(json_input_path, "r", encoding="utf-8") as file:
    data = json.load(file)

  df = data["df"]
  parameters = data["parameters"]
  policies = data["policies"]
  filters = apply_filters(json_input_path)
  # pylint: disable=unnecessary-lambda-assignment
  target_calculation = lambda x: ((x["total_price"]) * x["travelers"]).sum()
  top_n = data["top_n"]

  df = (
    pd.read_csv("./data/sample_tne_data_flights_and_hotel_combined.csv")
    .drop(["address", "amenities", "hotel_name"], axis=1)
    .groupby(["origin", "destination", "date_from", "date_to"])
    .aggregate("min")
    .reset_index()
  )

  result = optimize(
    df, parameters, policies, filters, target_calculation, top_n
  )

  for res, _ in result:
    assert isinstance(res, pd.DataFrame)
    assert "total_cost" in res.columns
    assert res["total_cost"].iloc[0] == expected_total_cost
    break

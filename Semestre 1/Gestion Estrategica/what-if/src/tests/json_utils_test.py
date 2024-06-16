#!/usr/bin/env python3

"""Test cases for the utility JSON policies for scenario testing.."""

# pylint: disable=wildcard-import, missing-function-docstring,
# pylint: disable=redefined-outer-name, unused-wildcard-import
# pylint: disable=bad-indentation

import json
import pytest

from what_if.tne.json_utils import read_json_filters
from what_if.tne.json_utils import filter_json
from what_if.tne.json_utils import pretty_print_json

@pytest.fixture
def json_filter_file(tmpdir):
  # Create a temporary JSON file with constraints
  filters = {
      "filters": {
      "date_from": ["2024-01-01"],
      "date_to": ["2024-01-10"],
      "flex_days": 2
      }
  }
  file_path = tmpdir.join("constraints.json")
  with open(file_path, "w",encoding="utf-8") as file:
    json.dump(filters, file)
  return file_path


def test_read_json_filters(json_filter_file):
  """
  This test function verifies the functionality of reading constraints from a JSON file. 
  It uses a temporary JSON file 
  created by the fixture 'json_constraints_file'. 
  The 'read_json_constraints' function located in 'src/what_if/json_utils.py'
  is called to read the JSON file. It checks whether 'date_from', 
  'date_to', and 'flex_days' are present in the constraints.
  """
  constraints = read_json_filters(json_filter_file)

  assert isinstance(constraints, dict)
  assert "date_from" in constraints
  assert "date_to" in constraints
  assert "flex_days" in constraints

def test_filter_json():
    """
    This test function verifies the functionality of filtering JSON data to include only specified keys.
    """
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }
    keys = ["name", "age"]
    filtered_data = filter_json(data, keys)

    assert isinstance(filtered_data, dict)
    assert "name" in filtered_data
    assert "age" in filtered_data
    assert "city" not in filtered_data
    assert filtered_data["name"] == "John Doe"
    assert filtered_data["age"] == 30

def test_pretty_print_json():
    """
    This test function verifies the functionality of pretty-printing JSON data.
    """
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }
    pretty_json = pretty_print_json(data)

    assert isinstance(pretty_json, str)
    assert json.loads(pretty_json) == data
#!/usr/bin/env python3

""" Utilities when working with JSON policies used for scenario testing."""

import json

from what_if.param_utils import create_date_range

def read_json_filters(file_path):
  """Utility function for reading JSON-formatted filters."""
  with open(file_path, "r", encoding="utf-8") as file:
    datefile = json.load(file)
    return datefile["filters"]
  
def filter_json(data, keys):
    """Filters the JSON data to include only the specified keys."""
    return {key: data[key] for key in keys if key in data}

def pretty_print_json(data):
    """Returns a pretty-printed JSON string for the given data."""
    return json.dumps(data, indent=4)
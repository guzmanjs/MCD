"""Test code to check all TNE scenarios"""
import json
import os
import sys
import pandas as pd
import pytest
from what_if.tne.scenario import Optimization
from what_if.tne.schema import Validation
from what_if.tne.cost_function import (estimate_flight_cost,
                                           estimate_hotel_cost)

DIR_SCENARIO_INPUT = "./src/what_if/tne/scenarios_combined"
DIR_SCENARIO_OUTPUT = "./src/what_if/tne/combined_scenario_output"
sys.path.append('.')

@pytest.mark.parametrize("input_filename, output_filename, expected_destination, expected_cost",
[
    ('sample_scenario13_body.json', 'scenario13_output.json', "Chicago", 11802)
])
def test_optimal_cost_destinations(input_filename, output_filename,
                                   expected_destination, expected_cost):
  """Function to test all scenarios"""
  input_file_path = os.path.join(DIR_SCENARIO_INPUT, input_filename)
  with open(input_file_path, 'r',encoding="utf-8") as file:
      input_json = json.load(file)

  output_file_path = os.path.join(DIR_SCENARIO_OUTPUT, output_filename)
  with open(output_file_path, 'r',encoding="utf-8") as file:
      expected_output = json.load(file)

  history_data = pd.read_csv("./data/combined_flight_and_hotel_data.csv",index_col=False)
  history_data["Date"] = pd.to_datetime(history_data['Date'], format="%Y-%m-%d")
  cost_function_list =[estimate_hotel_cost,estimate_flight_cost]
  response = Optimization(Validation(**input_json),history_data,cost_function_list).get_best_recommendations()
  response_data = response[0]
  assert response_data['Optimal_Destination'] == expected_destination, "Mismatch in Optimal Destination"
  assert response_data['Overall Cost'] == expected_cost, "Mismatch in Overall Cost"
  assert len(response_data['Details']) == len(expected_output[0]['Details']), "Mismatch in number of Details entries"

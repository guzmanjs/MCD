#!/usr/bin/env python3

"""Test cases for the main optimize function."""

from datetime import date

import pandas as pd
import pytest

from what_if.brute_force_general import optimize
from what_if.brute_force_general import keep_only_relevant_records
from what_if.brute_force_general import keep_only_filters
from what_if.brute_force_general import apply_cost_function
from what_if.brute_force_general import enumerate_over_all_parameters
from what_if.brute_force_general import merge_scenario_parameter_with_policy
from what_if.brute_force_general import enumerate_scenarios


@pytest.fixture
def sample_data_optimize():
  """Provides sample data to mimic the expected input for optimization."""
  return pd.DataFrame({
      'Origin': ['Seattle', 'San Francisco', 'Seattle', 'San Francisco', 'Chicago'],
      'Destination': ['NYC'] * 5,
      'Date': pd.date_range('2024-01-01', periods=5, freq='D'),
      'Flight_Price': [300, 400, 350, 450, 380],
      'Hotel_Price': [200, 220, 210, 230, 240]
  })


@pytest.fixture
def setup_cost_function_data():
    """Provides data for testing the cost function."""
    df = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=4, freq='D'),
        'Price': [100, 200, 300, 400],
        'Quantity': [1, 2, 3, 4]
    })
    policies = [
        {'Date': pd.Timestamp('2024-01-01'), 'Quantity': 1},  # Normal case
        {'Date': pd.Timestamp('2024-01-02'), 'Quantity': 2},  # Normal case
        {'Date': pd.Timestamp('2025-01-01'), 'Quantity': 10}  # Edge case: Date and quantity not in df
    ]
    target_calculation = lambda df: (df['Price'] * df['Quantity']).sum()  # Defining the lambda to calculate costs
    return df, policies, target_calculation


@pytest.fixture
def sample_data():
  """Create a sample DataFrame to mimic real data structure with appropriate 
    column names and data types
    for relevant records and  constraints."""
  return pd.DataFrame({
    'Origin': ['Seattle', 'Chicago', 'San Francisco', 'Los Angeles', 'San Diego'] * 5,
    'Destination': ['NYC'] * 25,
    'Date': pd.date_range(start='2024-01-03', periods=5, freq='D').repeat(5),
    'Flight_Price': [360, 250, 430, 430, 250] * 5,
    'Hotel_Name': [None] * 25,
    'Stars': [4, 5, 4, 5, 4] * 5,
    'Address': [None] * 25,
    'Amenities': [None] * 25,
    'Night_Price': [403, 1404, 403, 1404, 212] * 5
  })


@pytest.fixture
def policies():
  """Provides sample policy to mimic the expected input for relevant records and optimization. """
  return [{'Origin': 'Seattle'}, {'Origin': 'San Francisco'}]

@pytest.fixture
def policies_not_existent():
  """Provides sample policy to mimic the expected input for relevant records and optimization. """
  return [{'Origin': 'Miami'}, {'Origin': 'Alabama'}]

@pytest.fixture
def filters():
  """Adjust constraints to include proper column names used in filtering for keep constraints."""
  return {"Date": pd.to_datetime(['2024-01-03', '2024-01-20'])}


# Define fixture to load policy
@pytest.fixture
def policy():
  """Provides sample policy to mimic the expected input 
  for enumerate scenarios and scenario parameter with policy.
  """
  return [{'origin': 'NYC', 'travelers': 4},
          {'origin': 'Los Angeles', 'travelers': 8},
          {'origin': 'Chicago', 'travelers': 4}]


# Define fixture to load data from CSV
@pytest.fixture
def dfp():
  """Provides file csv to mimic the expected input for enumerate scenarios."""
  return pd.read_csv('./src/tests/test_data/all_combinations.csv')


@pytest.fixture
def setup_data():
  """Provides sample data to mimic the expected input for cost function."""
  data = {
    'origin': ['NYC', 'NYC', 'Los Angeles', 'Chicago'],
    'destination': ['Seattle', 'Seattle', 'Seattle', 'Seattle'],
    'date_from': ['2024-01-10', '2024-01-12', '2024-01-10', '2024-01-10'],
    'date_to': ['2024-01-16', '2024-01-16', '2024-01-16', '2024-01-16'],
    'flight_price': [173.0, 177.0, 61.0, 73.0],
    'stars': [5.0, 5.0, 5.0, 4.0],
    'hotel_price': [1387.0, 334.0, 1387.0, 217.0],
    'total_price': [1560.0, 511.0, 1448.0, 290.0],
    'travelers': [4, 4, 8, 4]
  }
  df = pd.DataFrame(data)
  policy_ = [
    {'origin': 'NYC', 'travelers': 4, 'destination': 'Seattle', 'date_from': '2024-01-10', 'date_to': '2024-01-16'},
    {'origin': 'Los Angeles', 'travelers': 8, 'destination': 'Seattle', 'date_from': '2024-01-10', 'date_to': '2024-01-16'},
    {'origin': 'Chicago', 'travelers': 4, 'destination': 'Seattle', 'date_from': '2024-01-10', 'date_to': '2024-01-16'}
  ]
  target_calculation = lambda x: ((x["total_price"]) * x["travelers"]).sum()

  return df, policy_, target_calculation

@pytest.fixture
def sample_df():
  """Provides sample data to mimic the expected input for parameter enumeration."""
  return pd.DataFrame({
      'origin': ['NYC', 'LA'],
      'destination': ['Seattle', 'Chicago'],
      'date_from': ['2024-01-01', '2024-01-02'],
      'date_to': ['2024-01-05', '2024-01-06']
  })


def test_optimize(sample_data_optimize, policies, filters, setup_data):
  """
  Evaluates the optimize function from the brute_force_general module. 
  This test verifies that the optimize function
  processes the data based on provided policies and constraints and 
  returns a limited set of top-performing scenarios
  based on cost, ensuring that the number of results returned does not exceed 
  the specified maximum (top_n).
  """
  target_calculation = setup_data # lambda function to calculate costs
  parameters = ['Origin', 'Destination', 'Date']
  top_n = 2  # Limit of results

  # Call the optimize function
  results = optimize(sample_data_optimize, parameters, policies, filters,target_calculation,top_n)

  # Check that the number of results does not exceed top_n
  assert len(results) <= top_n, "Should return at most top_n results"
  # Check that the results are tuples of (scenario, cost)
  assert all(isinstance(result, tuple) for result in results), "Each result should be a tuple containing scenario data and a cost"
  for result in results:
    assert isinstance(result[0], dict), "First element of each tuple should be a dictionary (the scenario)"
    assert isinstance(result[1], (int, float)), "Second element of each tuple should be a numeric type (the cost)"


def test_keep_only_relevant_records(sample_data, policies):
  """
  Tests keep_only_relevant_records function to ensure it correctly filters data 
  based on specified policies.
  This function verifies that the output only includes records that match the policy criteria.
  """
  expected_origins = set(policy['Origin'] for policy in policies)

  relevant_records = keep_only_relevant_records(sample_data, policies)

  assert all(rec in expected_origins for rec in relevant_records['Origin']), "Should only contain relevant origins"


def test_empty_keep_only_relevant_records (sample_data, policies_not_existent):
  """
  Tests the keep_only_relevant_records function to verify its behavior when no 
  relevant records match the given policies.
  This test ensures that the function returns an empty DataFrame when the policies 
  do not exist in the sample data,
  thus confirming the function's ability to correctly handle cases with no matching records.
  """
  relevant_records = keep_only_relevant_records(sample_data, policies_not_existent)

  assert relevant_records.empty, "The DataFrame should be empty when no records match the policy criteria"

def test_keep_only_filters(sample_data, filters):
  """
  Tests the keep_only_filters function to confirm that it accurately applies 
  specified constraints to the data.
  This test ensures that only records meeting the date constraints are returned.
  """

  formatted_constraints = {'Date': filters['Date'].tolist()}

  constrained_records = keep_only_filters(sample_data, formatted_constraints)

  assert all(filters['Date'][0] <= date <= filters['Date'][1] for date in constrained_records['Date']), "Dates should be within the constraints"
  assert not constrained_records.empty, "The DataFrame should not be empty after applying date constraints"


def test_enumerate_over_all_parameters(sample_df):
  """
  This test function verifies the functionality of the 'enumerate_over_all_parameters' 
  function located in src/what_if/brute_force_general.
  It checks whether all possible combinations of specified parameters are correctly 
  generated from a given DataFrame.
  The test defines multiple parameters and a sample DataFrame, 
  then it calls the function with these parameters,
  and checks if the resulting combinations match the expected set of combinations.
  """
  parameters = ['origin', 'destination', 'date_from', 'date_to']
  expected_combinations = [
    {'origin': 'NYC', 'destination': 'Seattle', 'date_from': '2024-01-01', 'date_to': '2024-01-05'},
    {'origin': 'NYC', 'destination': 'Seattle', 'date_from': '2024-01-01', 'date_to': '2024-01-06'},
    {'origin': 'NYC', 'destination': 'Seattle', 'date_from': '2024-01-02', 'date_to': '2024-01-05'},
    {'origin': 'NYC', 'destination': 'Seattle', 'date_from': '2024-01-02', 'date_to': '2024-01-06'},
    {'origin': 'NYC', 'destination': 'Chicago', 'date_from': '2024-01-01', 'date_to': '2024-01-05'},
    {'origin': 'NYC', 'destination': 'Chicago', 'date_from': '2024-01-01', 'date_to': '2024-01-06'},
    {'origin': 'NYC', 'destination': 'Chicago', 'date_from': '2024-01-02', 'date_to': '2024-01-05'},
    {'origin': 'NYC', 'destination': 'Chicago', 'date_from': '2024-01-02', 'date_to': '2024-01-06'},
    {'origin': 'LA', 'destination': 'Seattle', 'date_from': '2024-01-01', 'date_to': '2024-01-05'},
    {'origin': 'LA', 'destination': 'Seattle', 'date_from': '2024-01-01', 'date_to': '2024-01-06'},
    {'origin': 'LA', 'destination': 'Seattle', 'date_from': '2024-01-02', 'date_to': '2024-01-05'},
    {'origin': 'LA', 'destination': 'Seattle', 'date_from': '2024-01-02', 'date_to': '2024-01-06'},
    {'origin': 'LA', 'destination': 'Chicago', 'date_from': '2024-01-01', 'date_to': '2024-01-05'},
    {'origin': 'LA', 'destination': 'Chicago', 'date_from': '2024-01-01', 'date_to': '2024-01-06'},
    {'origin': 'LA', 'destination': 'Chicago', 'date_from': '2024-01-02', 'date_to': '2024-01-05'},
    {'origin': 'LA', 'destination': 'Chicago', 'date_from': '2024-01-02', 'date_to': '2024-01-06'}
  ]

  results = enumerate_over_all_parameters(sample_df, parameters)

  # Check the number of combinations
  assert len(results) == len(expected_combinations), "The number of generated combinations should match the expected number."
  # Check the content of the combinations
  for combo in expected_combinations:
    assert combo in results, f"Expected combination {combo} not found in results."
  # Ensure all results are unique
  assert len(results) == len(set(tuple(sorted(d.items())) for d in results)), "Results should contain unique combinations."


def test_cost_function(setup_data):
  """
  This test function checks if the function accurately calculates total costs 
  based on certain inputs and if the resultant DataFrame reflects the expected 
  outcomes based on the policies applied."""
  df, policy_, target_calculation = setup_data
  expected_total_cost = 1560*4 + 1448*8 + 290*4  # Adjust calculation as necessary

  result_df, total_cost = apply_cost_function(df, policy_, target_calculation)

  assert total_cost == expected_total_cost, "The total cost calculation is incorrect."
  assert len(result_df) == 3, "The number of entries in the result DataFrame is incorrect."


def test_apply_cost_function(setup_cost_function_data):
    """Tests the cost_function including edge cases."""
    df, policies, target_calculation = setup_cost_function_data

    # Test normal cases
    normal_results = []
    for policy in policies[:2]:
        result_df, total_cost = apply_cost_function(df, pd.DataFrame([policy]), target_calculation)
        normal_results.append((result_df.empty, total_cost, len(result_df)))
        assert not result_df.empty, "Resulting DataFrame should not be empty for matching cases."
        assert len(result_df) == len(pd.DataFrame([policy])), "Length of result_df should match the policy dataframe length."
        assert 'total_cost' in result_df.columns, "DataFrame should have a 'total_cost' column calculated."

    # Verify costs are as expected
    assert normal_results[0][1] == 100, "Total cost should be 100 for the first case."
    assert normal_results[1][1] == 400, "Total cost should be 400 for the second case."

    # Test edge case
    edge_result_df, edge_total_cost = apply_cost_function(df, pd.DataFrame([policies[2]]), target_calculation)
    assert edge_result_df.empty, "Resulting DataFrame should be empty for non-matching case."
    assert edge_total_cost == float('inf'), "Total cost should be infinite for non-matching case."
    assert len(edge_result_df) == 0, "Length of the DataFrame for the edge case should be zero."


def test_enumerate_scenarios(policy, dfp):
  """
  This test function verifies the behavior of the 'enumerate_scenarios' 
  function located at src/what_if/brute_force_general.
  It loads a policy and data frame, then calls the 'enumerate_scenarios' 
  function with these inputs.
  After that, it checks if the actual output matches the expected output.
  """
  parameters = ['destination', 'date_from', 'date_to']
  expected_output = [
    [
        {'origin': 'NYC', 'travelers': 4},
        {'origin': 'Los Angeles', 'travelers': 8},
        {'origin': 'Chicago', 'travelers': 4}
    ] * 2
  ]
  result = enumerate_scenarios(dfp, policy, parameters)

  actual_output = []
  # Iterate through the actual output and create dictionaries with only 'origin' and 'travelers'
  for trip_list in result:
    for trip in trip_list:
      expected_trip = {'origin': trip['origin'], 'travelers': trip['travelers']}
      actual_output.append(expected_trip)

  # Check if the result matches the expected output
  assert actual_output[:2] == expected_output[0][:2]
  # Check if the length of the result DataFrame is as expected (should match the length of policy entries that matched)
  assert len(result) == 54, "The number of entries in the result DataFrame is incorrect."


def test_merge_scenario_parameter_with_policy(policy):
  """
  This test function verifies the behavior of the 'merge_scenario_parameter_with_policy' 
  function located at src/what_if/brute_force_general.
  It defines a scenario parameter and an expected output based on merging this 
  parameter with the policy.
  Then, it calls the function with the scenario parameter and policy, 
  and checks if the result matches the expected output.
  """
  # Define scenario parameter
  scenario_parameter = {'destination': 'Los Angeles',
                        'date_from': '2024-01-12', 
                        'date_to': '2024-01-15'}

  # Define expected output based on merging scenario parameter with policy
  expected_output = [
      {'origin': 'NYC', 'travelers': 4, 'destination': 'Los Angeles',
       'date_from': '2024-01-12', 'date_to': '2024-01-15'},
      {'origin': 'Los Angeles', 'travelers': 8, 'destination': 'Los Angeles',
       'date_from': '2024-01-12', 'date_to': '2024-01-15'},
      {'origin': 'Chicago', 'travelers': 4, 'destination': 'Los Angeles',
       'date_from': '2024-01-12', 'date_to': '2024-01-15'}
  ]

  # Call the function and check if the result matches the expected output
  result = merge_scenario_parameter_with_policy(scenario_parameter, policy)

  assert result == expected_output

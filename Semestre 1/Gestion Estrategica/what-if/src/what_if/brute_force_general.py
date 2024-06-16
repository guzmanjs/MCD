#!/usr/bin/env python3

"""Primary module for the general optimization routine.

This module has a single function necessary for the optimization of the routine
(`optimize()`). You can import the module as so.

>>> from what_if.brute_force_general import optimize

"""

# pylint: disable=bad-indentation

import logging
from functools import reduce
from itertools import product
from typing import Sequence

import pandas as pd
from tqdm import tqdm

from what_if.keep_n import KeepN

# Setting up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# pylint: disable=too-many-arguments
def optimize(
  df,
  parameters,
  policies,
  filters,
  cost_function,
  top_n=3,
):
  """Optimization routine. For more information, consult the documentation at README.md.

  Args:
    df: pandas.DataFrame containing the data you want to optimize against.
    parameters: List[str]
        List of columns (passed as their name) you want to optimize. The function will
        return the optimal combination of parameters.
    policies: List[dict]
        A list of dictionaries that represents the elements that will be optimized.
        At least one of the keys must map to one column of `df.` A policy is a record that
        influence the optimization.
    filters: dict
        A dictionary mapping columns (by their name) to possible values.
        The filters are applied *before* any optimization and serve to reduce the number
        of scenarios evaluated.
    cost_function: Callable[[pd.Series], float]
        Cost function to be applied to a scenario to compute the cost of acting on the scenario.
        The optimization routine will return the approximate smallest value
        for the results of this function.
    top_n: int
        How many results do you want returned?

  Returns:
    A list of `top_n` tuples (the values and the associated cost as computed by `target_calculation`).
  """
  # We keep only the columns we care about
  try:
    if not set(parameters).issubset(set(df.columns)):
      raise ValueError("Columns provided in parameters does not match with dataset columns")

    # Columns in use for the policy
    policy_columns = list(
          reduce(lambda x, y: set(x).union(set(y)), [x.keys() for x in policies])
      )

      # We need to match on at least one column.
    if not set(policy_columns).intersection(set(df.columns)) != set():
      raise ValueError("No common columns found between policy_columns and df.columns")

    common_columns = list(set(parameters + policy_columns).intersection(df.columns))
    group_counts = df.groupby(common_columns).count().max().max()
    if not group_counts==1:
      raise ValueError("Group count is not equal to 1")

      # Remove any record which does not belong to the policy
    df = keep_only_relevant_records(df, policies)
    if filters:
      df = keep_only_filters(df, filters)

    # Optimization
    answer = KeepN(top_n)
    all_scenarios = enumerate_scenarios(df, policies, parameters)
    for scenario in tqdm(all_scenarios):
      answer.add_item(apply_cost_function(df, scenario, cost_function))

    return answer.return_results()

  except Exception as err:
    raise ValueError(f"An unexpected error occured during optimization: {err}") from err


def keep_only_relevant_records(df, policies):
  """From a DataFrame `df`, keep only the records that are relevant for
  computing the optimized parameters for a given set of policies."""
  return pd.concat(
    [df.merge(pd.DataFrame([x]), how="inner") for x in policies]
  ).drop_duplicates()


def keep_only_filters(df, policy):
  """From a DataFrame `df`, keep only the records that are relevant for
  computing the optimized parameters for a given set of filters."""
  def _wrap(item):
    return item if isinstance(item, list) else [item]

  return df[
    reduce(lambda x, y: x & y, [(df[x].isin(_wrap(y))) for x, y in policy.items()])
  ]


def apply_cost_function(df, policy, target_calculation):
  """Applies the cost function/target_calculation to a policy, using the data in `df`."""
  answer = df.merge(pd.DataFrame(policy), how="inner")
  if len(answer) != len(policy):
    return answer, float("inf")

  answer["total_cost"] = target_calculation(answer)

  return answer, target_calculation(answer)


# TODO: This could be more performant
def enumerate_over_all_parameters(
  dfp, parameters: Sequence[str] = ("destination", "date_from", "date_to", "stars")
):
  """Brute-force approach. Takes all the combinations of parameters and return
  a list of all the scenarios to evaluate."""
  def _tuple_to_dict(val):
    return {x[0]: x[1] for x in val}

  return [
    _tuple_to_dict(rec)
    for rec in product(
      *[
        [(parameter, value) for value in set(dfp[parameter])]
        for parameter in parameters
    ]
      )
  ]


def merge_scenario_parameter_with_policy(scenario_parameter, policy):
  """Merges the policy dictionary `pol` with the scenario created with
  `enumerate_over_all_parameters()`. The function is kept separate for
  tidyness and ease of testing."""
  return [pol | scenario_parameter for pol in policy]


# TODO: We could refine this further by only keeping the values in the data.
def enumerate_scenarios(
  dfp,
  policy,
  parameters: Sequence[str] = ("destination", "date_from", "date_to", "stars"),
):
  """Combination of `enumerate_over_all_parameters()` and
  `merge_scenario_parameter_with_policy()`."""
  return [
    merge_scenario_parameter_with_policy(scenario, policy)
    for scenario in enumerate_over_all_parameters(dfp, parameters)
  ]

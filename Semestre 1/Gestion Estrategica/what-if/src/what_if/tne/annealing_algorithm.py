""" Annealing Algorithm used for the T&E specific optimization."""

# pylint: disable=bad-indentation

import math
import random
import logging
from typing import Dict
from what_if.tne.cost_function import CalculateTripCost
from what_if.tne.utilities import (generate_neighboring_solution,
                        create_json_response)
from what_if.tne.custom_exceptions import (FlightEstimationError,
                               HotelEstimationError,
                               TripCalculationError,
                               AnnealingOptimizationError)

# Setting up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def select_common_destination(destination_lists) -> str:
  """to return random destination from list fo destinations"""
  # Find the intersection of all destination lists to ensure the selected
  # destination is available for all trips
  common_destinations = set(destination_lists[0]).intersection(*destination_lists[1:])
  # Randomly select one of the common destinations
  selected_destination = random.choice(list(common_destinations)) if common_destinations else None
  return selected_destination

def setup_initial_solution(solution,destination)-> list[Dict]:
  """ to set up initial solution"""
  # Extract all destination lists from trips
  common_destination = destination
  if common_destination is None:
    return None

  # Create initial_solution with selected common destination and solution details
  for sol in solution:
      sol.destination = common_destination
  return solution

def is_solution_unique(existing_solutions, new_solution) -> bool:
  """to filter unique solution from list of solutions"""
  for sol, _ in existing_solutions:
    if all(sol[origin] == new_solution[origin] for origin in sol):
      return False
  return True

def convert_to_tuple(item) -> tuple:
  """function to list/dict to tuple"""
  if isinstance(item, list):
    return tuple(convert_to_tuple(elem) for elem in item)
  elif isinstance(item, dict):
    return tuple((k, convert_to_tuple(v)) for k, v in item.items())
  return item

def annealing_algorithm_optimization(trips,destination_list,cost_evaluation_list,
                                     flex_days,data,initial_temperature=100,
                                     cooling_rate=0.1) -> list:
  """ Annealing Optimization method"""
  try:
      # Convert initial_solution dict to Trip objects for cost calculation
    logger.info("--Initiating annealing Algorithm--")
    potential_destinations = destination_list.copy()
    if len(trips) == 1 and trips[0].origin in destination_list:
      potential_destinations.remove(trips[0].origin)

    # Setup initial solution
    initial_solution= setup_initial_solution(trips,potential_destinations[0])
    initial_cost_details = [
        CalculateTripCost(trip, data, cost_evaluation_list).calculate_total_cost()
        for trip in initial_solution
    ]
    initial_cost = sum(detail["Trip Cost"] for detail in initial_cost_details)

    current_solution = initial_solution
    current_cost = initial_cost

    solutions = []
    temperature = initial_temperature
    best_destination = potential_destinations[0]

    while temperature > 0.0001:
      potential_destination = random.choice(potential_destinations)
      new_solution = [generate_neighboring_solution(sol, potential_destination,flex_days)
                      for sol in current_solution]
      new_cost_details = [CalculateTripCost(trip_obj,data,cost_evaluation_list).calculate_total_cost()
                          for trip_obj in new_solution]
      new_cost = sum(detail["Trip Cost"] for detail in new_cost_details)
      cost_difference = new_cost - current_cost
      acceptance_probability = math.exp(-cost_difference / temperature) if cost_difference >= 0 else 1.0

      if random.random() < acceptance_probability:
          current_solution = new_solution
          #current_cost = new_cost
          best_destination= potential_destination
          solutions.append((best_destination, new_cost, new_cost_details))

      temperature *= cooling_rate

    min_cost_trips={}
    for best_destination,cost, details in solutions:
      existing_cost, _ = min_cost_trips.get(best_destination, (float('inf'), None))
      if cost < existing_cost:
        min_cost_trips[best_destination] = (cost, details)

    solutions.sort(key=lambda x: x[1])
    top_solutions = solutions[:3]
    response = []
    for idx, (destination, cost, details) in enumerate(top_solutions, start=1):
      resp = create_json_response("Annealing Algorithm", idx, destination, cost, details)
      response.append(resp)
    logger.info("Annealing results: %s",response)
    return response

  except (FlightEstimationError, HotelEstimationError, TripCalculationError,Exception) as err:
    logger.error("Error occurred during tabu search optimization: %s", err)
    raise AnnealingOptimizationError(f"Error occurred during annealing optimization:{err}") from err

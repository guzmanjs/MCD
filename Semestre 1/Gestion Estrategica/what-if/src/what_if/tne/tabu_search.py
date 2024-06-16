"""Tabu search Algorithm"""
# from datetime import datetime, timedelta
import random
import logging
# import itertools
from what_if.tne.custom_exceptions import (FlightEstimationError,
                                TripCalculationError,
                                TabuOptimizationError,
                                HotelEstimationError)
from what_if.tne.utilities import (generate_neighboring_solution,
                        create_json_response)
from what_if.tne.cost_function import CalculateTripCost

# Setting up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def tabu_search_optimization(trips, destination_list,num_generations,iterations,
                             cost_evaluation_list,flex_days,data) -> list:
  """
  Perform tabu search optimization to find the best trip itinerary.

  Args:
      trips (list): List of Trip objects representing individual trips.
      destination_list (list): List of potential destinations.
      iterations (int, optional): Number of iterations for optimization. Default to 100.
      tabu_tenure (int, optional): Tabu tenure parameter. Default to 3.

  Returns:
      list: List of dict with optimized trip itineraries.

  Raises:
      TabuOptimizationError: If there is an error during tabu search optimization.
  """
  try:
    logger.info("--Initiating Tabu Search Algorithm--")
    history_data = data
    potential_destinations = destination_list.copy()
    min_cost_trips = {}
    # max_flex_days =max([trip.number_days_before_after for trip in trips])

    # if max_flex_days >=3 and len(trips)>=5 :
    #     num_generations = 50
    #     iterations = 100
    # elif max_flex_days >=3 and len(trips)>=3 :
    #     num_generations = 5 * max_flex_days -5
    #     iterations = 100 * max_flex_days -100
    # else :
    #     num_generations = num_generations
    #     iterations = iterations

    if len(trips) == 1 and trips[0].origin in destination_list:
      potential_destinations.remove(trips[0].origin)

    for _ in range(iterations):
      candidate_solutions = []
      potential_destination = random.choice(potential_destinations)

      for _ in range(num_generations):
        new_solution = [generate_neighboring_solution(sol, potential_destination,flex_days) for sol in trips]
        candidate_solutions.append(new_solution)

      for candidate in candidate_solutions:
        new_cost_list = [CalculateTripCost(cand,history_data,cost_evaluation_list).calculate_total_cost() for cand in candidate]
        combined_new_cost = sum(detail["Trip Cost"] for detail in new_cost_list)
        existing_cost, _ = min_cost_trips.get(potential_destination, (float('inf'), None))
        if combined_new_cost < existing_cost:
            min_cost_trips[potential_destination] = (combined_new_cost, new_cost_list)

    response = []

    sorted_min_cost_trips = sorted(min_cost_trips.items(), key=lambda x: x[1][0])
    recommendation = 1
    for destination, (total_cost, trip_details) in sorted_min_cost_trips[:3]:
      # for detail in trip_details:
      resp = create_json_response("Tabu Search",recommendation,destination, total_cost,trip_details)
      response.append(resp)
      recommendation +=1
    logger.info("Tabu Search Algortihm results : %s",response)
    return response

  except (FlightEstimationError, HotelEstimationError, TripCalculationError,Exception) as err:
    logger.error("Error occurred during tabu search optimization: %s",err)
    raise TabuOptimizationError(f"Error occurred during tabu search optimization: {err}") from err

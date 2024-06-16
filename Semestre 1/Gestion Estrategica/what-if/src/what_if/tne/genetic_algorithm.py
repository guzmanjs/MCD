"""Genetic Algorithm Module"""
import random
import numpy as np
import logging
from what_if.tne.cost_function import CalculateTripCost
from what_if.tne.utilities import (generate_neighboring_solution_ga,
                        create_json_response)
from what_if.tne.custom_exceptions import (GaFitnessError,
                               GaOptimizationError,
                               HotelEstimationError,
                               TripCalculationError,
                               FlightEstimationError)

# Setting up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class TravelOptimizerGA:
  """/"""
  def __init__(self,trips, potential_destinations,flex_days,cost_list,
                data,population_size=5, generations=8, mutation_rate=0.1):
      self.data = data
      self.trips = trips
      self.potential_destinations = []
      self.potential_destinations =potential_destinations
      self.population_size = population_size
      self.generations = generations
      self.mutation_rate = mutation_rate
      self.population = self.initialize_population()
      self.flex_days = flex_days
      self.cost_list = cost_list
      self.event_start_date =self.trips[0].start_date
      self.event_end_date =self.trips[0].end_date

  def initialize_population(self)  ->list:
    """Randomly destinations are chosen from a predefined list of possible destinations."""
    return [random.choice(self.potential_destinations) for _ in range(self.population_size)]

  def calculate_fitness(self, individual)  -> tuple:
    """The function calculates the total travel cost for given travel dates, 
      flight prices, and hotel rates for each destination in the population."""
    try:
      best_aggregate_cost = float('inf')
      best_aggregate_details = {}
      solution = self.trips.copy()

      new_solutions =generate_neighboring_solution_ga(solution,individual,self.flex_days)
      total_combination_cost = 0
      combined_trip_list = []
      for sol  in new_solutions:
        combined_trip_list = [CalculateTripCost(route,self.data,self.cost_list).calculate_total_cost() for route in sol]
        total_combination_cost=sum(detail["Trip Cost"] for detail in combined_trip_list)
        if total_combination_cost < best_aggregate_cost and total_combination_cost != 0:
            best_aggregate_cost = total_combination_cost
            best_aggregate_details = combined_trip_list

      return -best_aggregate_cost,best_aggregate_details if best_aggregate_details else {}
    except (FlightEstimationError,HotelEstimationError,TripCalculationError,Exception) as err:
      raise GaFitnessError(f"Error occurred during calculating fitness part of GA optimization: {err}") from err

  def evolve(self):
    """After fitness evaluation, the GA selects individuals to form a new generation. 
      This selection is based on their fitness scores. 
      The best-performing individuals (i.e., those with the lowest costs) are more 
      likely to be selected as parents for the next generation."""
    try:
      logger.info("--Initiate genetic Algorithm--")
      history = []
      all_solutions = []

      for _ in range(self.generations):
        current_gen_scores = []
        for individual in self.population:
          cost, details = self.calculate_fitness(individual)
          history.append((individual, -cost,details))
          current_gen_scores.append((-cost, individual))

        current_gen_scores.sort(reverse=True)

        parents = [ind for _, ind in current_gen_scores[:max(2, len(self.population)//2)]]

        new_population = []
        while len(new_population) < self.population_size:
          if len(parents) >= 2:
            parent1, parent2 = np.random.choice(parents, 2, replace=False)
          else:
            parent1 = parent2 = parents[0]
          child = self.crossover(parent1, parent2)
          child = self.mutate(child)
          new_population.append(child)

        self.population = new_population

      unique_solutions = {}
      for individual, cost,details in sorted(history, key=lambda x: x[1]):
        if individual not in unique_solutions:
          unique_solutions[individual] = cost
          all_solutions.append((individual, cost,details))
        if len(unique_solutions) == len(self.potential_destinations):
          break

      top_3_solutions = sorted(all_solutions, key=lambda x: x[1])[:3]
      recommendation = 1
      response = []
      for destination,cost,trip_details in top_3_solutions:
        # for detail in trip_details:
        resp =create_json_response("Genetic Algorithm",recommendation,destination,cost,trip_details)
        response.append(resp)
        recommendation +=1
      logger.info("Genetic alogrithm results: %s",response)
      return response
    except (GaFitnessError,Exception) as err:
      logger.error("Error occurred during GA optimization: %s",err)
      raise GaOptimizationError(f"Error occurred during GA optimization: {err}") from err

  def crossover(self, parent1, parent2):
    """For each new individual in the next generation, 
      two parents are selected based on their fitness."""
    return parent1 if np.random.rand() < 0.5 else parent2

  def mutate(self, individual):
    """Mutation randomly alters the destination of the offspring, 
      introducing new traits into the population."""
    if np.random.rand() < self.mutation_rate:
      return np.random.choice(self.potential_destinations)
    return individual

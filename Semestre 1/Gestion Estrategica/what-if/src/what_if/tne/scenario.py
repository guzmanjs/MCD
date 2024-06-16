"""Module calling different algorithm and returning best of three"""
import concurrent.futures
from copy import deepcopy
import pandas as pd
import logging
from what_if.tne.tabu_search import tabu_search_optimization
from what_if.tne.annealing_algorithm import annealing_algorithm_optimization
from what_if.tne.custom_exceptions import (DataError,
                                ConcurrentOptimizationError)
from what_if.tne.config import Config
from what_if.tne.genetic_algorithm import TravelOptimizerGA

# Setting up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Optimization(Config):
  """/"""
  def __init__(self,input_attr,data,cost_function):
    self.trips = input_attr.trips
    self.budget = input_attr.budget
    self.potential_destinations = input_attr.potential_destinations
    self.algorithms = input_attr.algorithms
    self.cost_evaluation_list = cost_function
    self.flex_days = input_attr.number_days_before_after
    self.data=data
    '''
    Generate results out from different optimizers.
    Returns the best results

    '''

  def historical_data(self) -> pd.DataFrame:
    """
    Read csv having price data for flights and hotels. 
    
    Returns:
        flight_history_data (pd.DataFrame) 
        hotel_history_data (pd.DataFrame) 
    """
    try:
      # file_path = os.path.join(self.path,self.filename)
      history_data=deepcopy(self.data)
      # history_data = pd.read_csv(file_path).drop_duplicates()
      # history_data['Date'] = pd.to_datetime(history_data['Date'], format="%Y-%m-%d")
      return history_data
    except FileNotFoundError as err:
      raise DataError("data file not found.") from err
    except pd.errors.EmptyDataError as err:
      raise DataError("data file is empty.") from err
    except pd.errors.ParserError as err:
      raise DataError("Error parsing data.") from err
    except Exception as err:
      raise DataError(f"An unexpected error occurred while reading data: {err}") from err

  def tabu_search(self,_) -> list:
    ''' Initializing Tabu Search Optimize'''

    tb_output =tabu_search_optimization(self.trips, self.potential_destinations,
                                      self.num_gen,self.iterations,
                                      self.cost_evaluation_list,self.flex_days,
                                      data=deepcopy(self.data))
    return tb_output

  def annealing_algorithm(self,_) -> list:
    """ Call Annealing algorithm for best fit value
        """
    # created separate function to modify hyperparemeter based on problem
    an_output = annealing_algorithm_optimization(self.trips,self.potential_destinations,
                                              self.cost_evaluation_list, self.flex_days,
                                              data=deepcopy(self.data),
                                              initial_temperature=self.initial_temperature,
                                              cooling_rate=self.cooling_rate)

    return an_output

  def genetic_algorithm(self,_) -> list:
    """Initializing Genetic Optimization"""
    optimizer = TravelOptimizerGA(self.trips, self.potential_destinations,
                                  self.flex_days,self.cost_evaluation_list,
                                  data=deepcopy(self.data),population_size=self.population_size,
                                  generations=self.generations, mutation_rate=self.mutation_rate)

    ga_output = optimizer.evolve()
    return ga_output

  def get_best_recommendations(self) -> list:
    """Using multiprocessing calling all the mentioned algorithm concurrently.
      accumulating all the results and filtering out the top three best fit values"""
    try:
      logger.info("starting multiple threading execution for algorithms: %s",self.algorithms)
      overall_response=[]
      results=[]
      with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_worker) as executor:
        for algo in self.algorithms:
          if algo == "Tabu Search":
            # Submit tasks for Tabu Search
            tabu_search_tasks =[executor.submit(self.tabu_search, i) for i in range(self.ite_range)]
            overall_response.extend(tabu_search_tasks)
          elif algo == "Annealing":
            # Submit tasks for Annealing
            annealing_tasks = [executor.submit(self.annealing_algorithm,j) for j in range(self.ite_range)]
            overall_response.extend(annealing_tasks)

          elif algo == "Genetic Algorithm":
            # Submit tasks for Genetic Algorithm
            ga_tasks = [executor.submit(self.genetic_algorithm,k) for k in range(self.ite_range)]
            overall_response.extend(ga_tasks)

        # Gather results
        for future in concurrent.futures.as_completed(overall_response):
          results.extend(future.result())

      min_costs = {}

      # return overall_response
      for row in results:
        recommendation = row['Recommendations']
        overall_cost = row['Overall Cost']
        if recommendation not in min_costs or overall_cost < min_costs[recommendation]:
          min_costs[recommendation] = overall_cost

      min_cost_rows =[row for row in results if row['Overall Cost'] == min_costs[row['Recommendations']]]
      sorted_recommendations = sorted(min_cost_rows,key=lambda x: x["Recommendations"])
      logger.info("Overall Scenario results: %s",sorted_recommendations)
      return sorted_recommendations

    except Exception as err:
      logger.error("An unexpected error occurred during running optimization in concurrent: %s",err)
      raise ConcurrentOptimizationError(f"An unexpected error occurred during running optimization in concurrent: {err}") from err

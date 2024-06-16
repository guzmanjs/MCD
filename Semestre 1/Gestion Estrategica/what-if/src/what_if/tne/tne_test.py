""" Test cases for TNE code"""
from datetime import datetime , date
import pandas as pd
import pytest
# Import your functions here
from what_if.tne.schema import Trip
from what_if.tne.tabu_search import tabu_search_optimization
from what_if.tne.cost_function import (CalculateTripCost,
                                           estimate_flight_cost,
                                           estimate_hotel_cost)
from what_if.tne.utilities import (generate_neighboring_date,
                                       generate_neighboring_solution,
                                       create_json_response)
from what_if.tne.genetic_algorithm import TravelOptimizerGA


@pytest.fixture
def dummy_flight_data() ->pd.DataFrame:
  """/"""
  dummy_data = pd.DataFrame({
      'Date': [datetime(2024, 4, 1), datetime(2024, 4, 2),datetime(2024, 4, 3),
                datetime(2024, 4, 4),datetime(2024, 4, 5), datetime(2024, 4, 6),
                datetime(2024, 4, 7),datetime(2024, 4, 8),datetime(2024, 4, 1),
                datetime(2024, 4, 2),datetime(2024, 4, 3),datetime(2024, 4, 4),
                datetime(2024, 4, 5),datetime(2024, 4, 6),datetime(2024, 4, 7),
                datetime(2024, 4, 8)],
      'Origin': ['Chicago','Chicago','Chicago','Chicago','Seattle','Seattle','Seattle','Seattle',
                  'Chicago','Chicago','Chicago','Chicago','NYC','NYC','NYC','NYC'],
      'City': ['Seattle', 'Seattle','Seattle', 'Seattle','Chicago', 'Chicago','Chicago', 
                'Chicago','NYC', 'NYC','NYC', 'NYC','Chicago', 'Chicago','Chicago','Chicago'],
      'Flight Price': [1000, 2000,550,660,200,400,800,1200,
                        800, 1500,400,800,300,150,1200,1000]
  })
  dummy_data['Date'] = pd.to_datetime(dummy_data['Date'], format="%d-%m-%Y")
  return dummy_data

@pytest.fixture
def dummy_hotel_data():
  """Mocking hotel History data"""
  dummy_data = pd.DataFrame({
      'Date': [datetime(2024, 4, 1), datetime(2024, 4, 2),datetime(2024, 4, 3),
                datetime(2024, 4, 4),datetime(2024, 4, 5), datetime(2024, 4, 6),
                datetime(2024, 4, 7),datetime(2024, 4, 8),datetime(2024, 4, 1),
                datetime(2024, 4, 2),datetime(2024, 4, 3),datetime(2024, 4, 4),
                datetime(2024, 4, 5), datetime(2024, 4, 6),datetime(2024, 4, 7),
                datetime(2024, 4, 8)],
      'City': ['Seattle', 'Seattle','Seattle','Seattle','Seattle','Seattle','Seattle','Seattle',
                      'NYC', 'NYC','NYC','NYC','NYC','NYC','NYC','NYC'],
      'Stars': [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
      'Night Price($)': [150, 250,55,60,200,250,70,50,
                          165, 220,70,40,250,220,75,60]
  })
  dummy_data['Date'] = pd.to_datetime(dummy_data['Date'], format="%d-%m-%Y")
  return dummy_data



# Test cases for estimate_flight_cost function
def test_estimate_flight_cost(dummy_flight_data):
  """test estimate_flight_cost function"""
  # with pytest.raises(FlightEstimationError):
  response = {}
  cost = estimate_flight_cost(Trip(origin="Chicago",destination= "Seattle",
                                    start_date= "2024-04-03",end_date= "2024-04-06",
                                    num_travelers= 1), dummy_flight_data, response)
  assert cost == 950

# Test cases for estimate_hotel_cost function
def test_estimate_hotel_cost(dummy_hotel_data):
  """ testing estimate_hotel_cost function"""
  response ={}
  rate =   estimate_hotel_cost(Trip(origin="Chicago",destination= "Seattle",
                                    start_date= "2024-04-03",end_date= "2024-04-04",
                                    num_travelers= 1),
                                      dummy_hotel_data,response)
  assert rate == 55

# Test cases for calculate_trip_cost function
def test_calculate_trip_cost(dummy_flight_data,
                             dummy_hotel_data):
  """Testing calculate_trip_cost function"""
  combined_dataset = pd.merge(dummy_flight_data,dummy_hotel_data,on=["Date","City"])
  cost_list=[estimate_flight_cost,estimate_hotel_cost]
  cost = CalculateTripCost(Trip(origin="Chicago",destination= "Seattle",
                                        start_date= "2024-04-03",end_date= "2024-04-05",
                                        num_travelers= 1),
                                  combined_dataset,cost_list).calculate_total_cost()
  assert cost['Trip Cost'] == 5665


# Test case for generate_neighboring_solution function
def test_generate_neighboring_solution():
  """ testing generate_neighboring_solution function 
    to check if return proper new solution """
  trip = Trip(origin="A",destination= "X",start_date= "2024-04-03",
              end_date= "2024-04-04",num_travelers= 1)
  potential_destination = "Y"
  solution = generate_neighboring_solution(trip, potential_destination,flex_days=1)
  assert solution.destination == potential_destination


def test_generate_neighboring_date_within_range():
  """To check if it returns correct date within range"""
  travel_date = date(2024, 4, 1)
  number_days_before_after =1
  new_date = generate_neighboring_date(travel_date,number_days_before_after)
  assert (new_date - travel_date).days in range(-3, 1)

def test_generate_neighboring_date_within_range_return_flag():
  """To check if it returns correct date within range"""
  travel_date = date(2024, 4, 1)
  number_days_before_after = 2
  new_date = generate_neighboring_date(travel_date,number_days_before_after, return_flag=True)
  assert (new_date - travel_date).days in range(0, 4)


# Test case for tabu_search_optimization function
def test_tabu_search_optimization(dummy_flight_data,
                             dummy_hotel_data):
  """To check Tabu Optimization functionality"""
  dataset = pd.merge(dummy_flight_data,dummy_hotel_data,on=["Date","City"])
  trips = [Trip(origin="Chicago",destination= "Seattle",
                start_date= "2024-04-03",end_date= "2024-04-04",
                num_travelers= 1)]
  destination_list = ["Seattle", "NYC"]
  flex_days=1
  cost_list=[estimate_flight_cost,estimate_hotel_cost]
  result = tabu_search_optimization(trips, destination_list,5,50,cost_list,flex_days,dataset)
  assert isinstance(result, list)
  assert result[0]["Optimal_Destination"] == "NYC"

def test_genetic_algorithm(dummy_flight_data,
                             dummy_hotel_data):
  """"To check Genetic Algorithm functionality"""
  dataset = pd.merge(dummy_flight_data,dummy_hotel_data,on=["Date","City"])
  trips = [Trip(origin="Chicago",destination= "Seattle",
                start_date= "2024-04-03",end_date= "2024-04-04",
                num_travelers= 1)]
  destination_list = ["Seattle", "NYC"]
  flex_days=1
  cost_list=[estimate_flight_cost,estimate_hotel_cost]
  optimizer = TravelOptimizerGA(trips,destination_list,
                                    flex_days,cost_list,
                                    dataset,population_size=5,
                                    generations=8, mutation_rate=0.1)

  result = optimizer.evolve()
  assert isinstance(result, list)
  assert result[0]["Optimal_Destination"] == "NYC"

# Test cases for create_json_response function
def test_create_json_response():
  """test response body"""
  rec =1
  location = "Test Location"
  cost = 100
  details = {"test_detail": "value"}
  response = create_json_response("Tabu Search",rec,location, cost, details)
  assert response["Optimal_Destination"] == location
  assert response["Overall Cost"] == cost
  assert response["Details"] == details

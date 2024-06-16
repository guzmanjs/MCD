"""Configuration module"""

class Config:
  """where all algorithm parameters are define"""
  path = "data"
  filename = "combined_flight_and_hotel_data.csv"

  # variables for Multi processing
  max_worker = 12
  ite_range = 1

  # Tabu Search  Algorithm
  iterations= 100
  num_gen =20

  #Annealing Algorithm
  initial_temperature=200
  cooling_rate=0.1
  n=3

  # Genetic Algorithm
  population_size=5
  generations=8
  mutation_rate=0.1

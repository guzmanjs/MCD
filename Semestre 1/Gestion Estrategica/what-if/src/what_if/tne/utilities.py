"""/"""
import json
from datetime import datetime, timedelta
import random
from copy import deepcopy
import pandas as pd
import numpy as np


def generate_neighboring_date(travel_date,number_days_before_after,return_flag=False)-> datetime.date:
  """
  Generate a neighboring date within a small range around the given travel date.

  Args:
      travel_date (datetime.date): The base travel date.
      number_days_before_after (int) : Range value to consider to generate 
                                        a new date from the travel_date
      return_flag (bool, optional): Indicates if it's for a return trip. Defaults to False.

  Returns:
      datetime.date: The generated neighboring date.

  """
  if return_flag is False:
    days_to_add = random.randint(-number_days_before_after,0)
  else:
    days_to_add = random.randint(0,number_days_before_after)
  datetime_obj = datetime.combine(travel_date, datetime.min.time())
  new_date = (datetime_obj+ timedelta(days=days_to_add)).date()
  if abs((new_date -travel_date).days) >10:
    return travel_date

  return new_date

def generate_neighboring_solution(trip, potential_destination,flex_days) -> object:
  """
  Generate new trip details with new dates and potential destination
  Args:
      trip (Trip): Trip object containing trip details.
      potential_destination (str): destination selected with random choice
      flex_days (int) : Range value to consider to generate a new date from the travel_date

  Returns:
      dict : new trip details. 
  """
  trips_copy = deepcopy(trip)
  if flex_days:
    trips_copy.start_date = generate_neighboring_date(trips_copy.start_date,flex_days)
    trips_copy.end_date = generate_neighboring_date(trips_copy.end_date,flex_days,return_flag=True)
    trips_copy.destination = potential_destination
  else:
    trips_copy.destination = potential_destination
  return trips_copy

def generate_neighboring_solution_ga(trips,destination,flex_days):
  """
  Generate new trip details with new dates and potential destination for GA algorithm
  Args:
      trip (Trip): Trip object containing trip details.
      potential_destination (str): destination selected with random choice
      flex_days (int) : Range value to consider to generate a new date from the travel_date

  Returns:
      dict : new trip details. 
  """
  overall_combinations_trips =[]
  if flex_days:
    event_start_date =trips[0].start_date
    event_end_date =trips[0].end_date
    departure_dates = pd.date_range(start=event_start_date - pd.Timedelta(days=flex_days), end=event_start_date)
    return_dates = pd.date_range(start=event_end_date, end=event_end_date + pd.Timedelta(days=flex_days))

    for departure_date in departure_dates:
      for return_date in return_dates:
        if departure_date >= return_date:
          continue

        trips_copy = deepcopy(trips)
        departure_date = pd.to_datetime(departure_date, format="%Y-%m-%d")
        return_date = pd.to_datetime(return_date, format="%Y-%m-%d")
        for trip in trips_copy:
          trip.start_date = departure_date
          trip.end_date = return_date
          trip.destination = destination

        overall_combinations_trips.append(trips_copy)
  else:
    for trip in trips:
      trip.destination = destination
    overall_combinations_trips.append(trips)

  return overall_combinations_trips

def create_json_response(algorithm,rec,location,cost,details) -> dict:
  """to return response in dictionary format"""
  output ={"Algorithm":algorithm,
      "Recommendations": rec,
      "Optimal_Destination": location,
      "Overall Cost":cost,
      "Details":details
            }
  return output

def create_detailed_response(resp_list) -> list:
  """to return detailed response in provide api response in excel"""
  resp=[]
  for i in resp_list:
    for detail in i["Details"]:
      output ={"Algorithm":i["Algorithm"],
      "Recommendations": i["Recommendations"],
      "Optimal_Destination": i["Optimal_Destination"],
      "Overall Cost":i["Overall Cost"]
          }
      output.update(detail)
      resp.append(output)
  return resp

def convert_int64_to_int(obj) -> object:
  """/"""
  if isinstance(obj, np.int64):
    return int(obj)
  return obj

def generate_response(output)-> json:
  """Removing duplicates for final response"""
  seen= set()
  # Removing duplicates from various algorithms if present
  final_output = [item for item in output if (item["Recommendations"] not in seen)
                  and not seen.add(item["Recommendations"])]
  json_output = json.dumps(final_output,default=convert_int64_to_int).encode('utf-8')

  return json_output

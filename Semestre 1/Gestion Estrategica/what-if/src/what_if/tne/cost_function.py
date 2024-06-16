"""Cost Function Module"""
from datetime import datetime ,date
import pandas as pd
from what_if.tne.custom_exceptions import (TripCalculationError,
                                HotelEstimationError,
                                FlightEstimationError)


# Function to estimate flight cost from historical data

def estimate_flight_cost(trip, data,response) -> int:
  """
  Estimate the cost of a flight for a given trip and travel date.

  Args:
      trip (Trip): Trip object containing trip details.
      data (pd.DataFrame): DataFrame containing flight data.
      travel_date (str): Travel date 
      return_flag (bool, optional): Indicates if it's a return flight. Default to False.

  Returns:
      float: Estimated flight cost.

  Raises:
      FlightEstimationError: If there is an error estimating flight cost.
  """
  def flight_cost_1(origin,destination,travel_date):
      default_flight_cost = 5000
      matching_flights = data[(data['Origin'] == origin) & (data['City'] == destination) &
                            (data['Date'] == travel_date)]
      if matching_flights.empty:
        return default_flight_cost
      return matching_flights['Flight Price'].min()
  try:

    if trip.origin == trip.destination:
      flight_cost = 0
      response.update({"Flight Rate":0,
                      "Flight Cost":0,
                      "Return Flight Rate":0,
                      "Return Flight Cost":0})
      return 0
    # for travel start date
    desired_date = pd.to_datetime(trip.start_date)
    return_desired_date = pd.to_datetime(trip.end_date)
    flight_rate = flight_cost_1(trip.origin,trip.destination,desired_date)
    # for flight cost for return date
    origin, destination = (trip.destination, trip.origin)
    return_flight_rate = flight_cost_1(origin,destination,return_desired_date)
    flight_cost = flight_rate * trip.num_travelers
    return_flight_cost = return_flight_rate * trip.num_travelers
    total_flight_cost = flight_cost +return_flight_cost
    response.update({"Flight Rate":flight_rate,
                    "Flight Cost":flight_cost,
                    "Return Flight Rate":return_flight_rate,
                    "Return Flight Cost":return_flight_cost})
    return total_flight_cost

  except Exception as err:
    raise FlightEstimationError(trip,trip.start_date,err) from err

def estimate_hotel_cost(trip, data,response,stars=None) -> int:
  """
  Estimate the cost of hotels for a given trip and hotel data.

  Args:
      trip (Trip): Trip object containing trip details.
      data (pd.DataFrame): DataFrame containing hotel data.
      stars (int, optional): Minimum star rating of hotels. Default to 4.

  Returns:
      tuple: A tuple containing total hotel cost and a list of hotel rates.

  Raises:
      HotelEstimationError: If there is an error estimating hotel cost.
  """
  try:
    default_hotel_cost = 15000
    if trip.origin == trip.destination:
      overall_hotel_cost = 0
      response.update({"Hotel Cost":overall_hotel_cost,
                      "Hotel cost per person":0,
                      "Hotel Rates":[]
                          })
    else:
      start_date = pd.to_datetime(trip.start_date)
      end_date = pd.to_datetime(trip.end_date)
      end_date = end_date - pd.Timedelta(days=1)
      matching_hotels = data[(data['City'] == trip.destination) &
                           (data['Date'].between(start_date, end_date))]
      if stars is not None:
        matching_hotels = matching_hotels[matching_hotels['Stars'] == stars]

      matching_hotels = matching_hotels.loc[matching_hotels.groupby('Date')
                                            ['Night Price($)'].idxmin()]
      hotel_rates = matching_hotels[["Date", "Night Price($)"]]

      if hotel_rates.empty:
        overall_hotel_cost = default_hotel_cost * trip.num_travelers * trip.max_nights
      else:
        hotel_cost = hotel_rates['Night Price($)'].sum()
        overall_hotel_cost = hotel_cost * trip.num_travelers
      hotel_rates_copy = hotel_rates.copy()
      hotel_rates_copy["Date"] = hotel_rates_copy["Date"].astype(str)
      response.update({"Hotel Cost":overall_hotel_cost,
                      "Hotel cost per person": hotel_rates['Night Price($)'].sum(),
                      "Hotel Rates":hotel_rates_copy.to_dict("records")
                          })
    return overall_hotel_cost

  except Exception as err:
    raise HotelEstimationError(trip,trip.start_date,err) from err

#Cost function Object
class CalculateTripCost():
  """ 
  Calculate the total cost of a trip including flight and hotel costs.

  Args:
      trip (Trip): Trip object containing trip details.
      flight_history_data (pd.DataFrame): DataFrame containing historical flight data.
      hotel_history_data (pd.DataFrame): DataFrame containing historical hotel data.

  Returns:
      dict: Dictionary containing trip cost details.

  Raises:
      TripCalculationError: If there is an error calculating trip cost.
  """
  def __init__(self,trip,data,cost_list):
      self.trip = trip
      self.data =data
      self.cost_list= cost_list
      self.total_cost = 0
      self.response={}
      for field_name, field_value in trip.__dict__.items():
        if field_value is not None:
          if isinstance(field_value, (datetime, date)):
            field_value = str(field_value)
          self.response.update({f"{field_name}":field_value})

  def calculate_total_cost(self) -> dict:
    """Summing up return values for all cost functions and returning overall value for a solution"""
    try:
      for cost_type in self.cost_list:
        cost = cost_type(self.trip, self.data, self.response)
        self.total_cost = self.total_cost + cost
      self.response.update({"Trip Cost":self.total_cost})
      return self.response

    except (FlightEstimationError, HotelEstimationError,Exception) as err:
      raise TripCalculationError(f"Error occurred while calculating trip cost: {err}") from err

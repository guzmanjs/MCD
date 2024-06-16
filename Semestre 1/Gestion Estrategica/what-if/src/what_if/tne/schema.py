""" Schema used for the TNE optimization around prospective scenarios."""

# pylint: disable=bad-indentation

from datetime import date
from typing import List, Optional, Union
from pydantic import BaseModel


class Trip(BaseModel):
  """Input Parameter Mandate/Optional"""
  origin : str
  destination : Union[str,List]
  start_date : date
  end_date : date
  num_travelers : int
  # additional attributes
  max_nights : Optional[int]  = None
  flight_class : Optional[str] = None
  airline : Optional[str] = None
  time_of_flight : Optional[str] = None
  hotel_stars : Optional[int] = None
  amenities : Optional[List] = None


class Validation(BaseModel):
  """/"""
  trips: List[Trip]  # it will have values like (origin,destination,date,no. of
                     # nights ,hotel) for each passenger
  budget :Optional[int] = None
    # only in case of multiple traveler
  number_days_before_after : int = 0
  potential_destinations : Optional[List] = None
  algorithms : List[str] = ["Tabu Search","Annealing"]

# @validator('traveler')
# def validate_traveler_keys(cls,v):
#     allowed_keys = {"orgin","destination","travel_date","max_nights","flight_class",
#     "airline","time_of_flight","hotel_stars","amenities"}
#     for key in v.keys():
#         if key not in allowed_keys:
#             raise ValueError(f"Key '{key}' is not allowed")

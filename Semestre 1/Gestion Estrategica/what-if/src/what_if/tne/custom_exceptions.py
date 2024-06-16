"""Custom Exceptions"""
class DataError(Exception):
  """Data error"""

class FlightEstimationError(Exception):
  """Error during estimating flight cost"""
  def __init__(self,trip,travel_date,e):
    self.details = {"Origin":trip.origin,
                    "Destination":trip.destination,
                    "Date":travel_date,
                    "error":e}
  def __str__(self):
    return f"{self.details}"

class TotalCalculationError(Exception):
    """Error during total cost calculation"""

class HotelEstimationError(Exception):
  """error during hotel cost estimation"""
  def __init__(self,trip,travel_date,e):
    self.details = {"Origin":trip.origin,
                    "Destination":trip.destination,
                    "Date":travel_date,
                    "error":e}
  def __str__(self):
    return f"{self.details}"

class TripCalculationError(Exception):
  """/"""

class TabuOptimizationError(Exception):
  """/"""

class AnnealingOptimizationError(Exception):
  """/"""

class GaFitnessError(Exception):
  """/"""

class GaOptimizationError(Exception):
  """/"""

class ConcurrentOptimizationError(Exception):
  """/"""

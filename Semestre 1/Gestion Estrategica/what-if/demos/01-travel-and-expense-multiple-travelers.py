#!/usr/bin/env python3

"""Demo 01: Travel and Expenses, multiple travelers.

In this scenario, we are considering the optimal travel destination from a group
of travelers. We assume that every traveler is going to the same destination,
leaving and retrurning on the same date. We provide some flexibility around the
departure and the return date.

"""

# pylint: disable=missing-function-docstring
# pylint: disable=bad-indentation

# The following are used because it makes the file clearer to read.
# pylint: disable=invalid-name, line-too-long, unnecessary-lambda-assignment
import os
import sys
import pandas as pd

from what_if.brute_force_general import optimize
from what_if.param_utils import create_date_range

# Step 1: Identify and prepate the data.
#
# We read the data from the original source. Because not every combination of
# the parameters (destination, date from, and date to) that we wish to use
# doesn't have a unique record, we need to simplify the data frame to keep the
# minimum price for every combination. We justify this that a traveler would
# pick the cheapest price for a given trip.
my_df = (
    pd.read_csv("./data/sample_tne_data_flights_and_hotel_combined.csv")
    .drop(["address", "amenities", "hotel_name"], axis=1)
    .groupby(["origin", "destination", "date_from", "date_to"])
    .aggregate("min")
    .reset_index()
)


my_parameters = ["destination", "date_from", "date_to"]

# Step 2: Create the policy, filters, and cost function
#
# In our scenario, we have four travelers leaving from NYC, eight travelers
# leaving from Los Angeles, and four travelers leaving from Chicago. Note that
# the `origin` field matches the `origin` field in the data frame. Any field
# part of the policy can't be a parameter because it is fixed: you can't
# optimize where the travelers come from in this scenario, nor can you change
# the number of travelers.
my_policy = [
    {"origin": "NYC", "travelers": 4},
    {"origin": "Los Angeles", "travelers": 8},
    {"origin": "Chicago", "travelers": 4}
]

# Because we want to provide a flexible departure and arrival for the group,
# we use the helper function `what_if.param_utils.create_date_range` to create a
# range of admissible dates and filter our data frame. This improves the
# performance by rejecting the records beyond the range. You could also
# provide a list of values.
#
# IMPORTANT: The data frame has dates as "objects" here, which is why we
# created a utility function that returns the values as a ISO-8601 formatted
# string.

my_filters = {"date_from": create_date_range("2024-01-12", -2),
              "date_to": create_date_range("2024-01-15", 2)
              }


# The cost function here is the total of the trips. We need to sum the
# multiplication of the total cost by the number of travelers.
my_cost_function = lambda s: (s["total_price"] * s["travelers"]).sum()

# How many top records do we want to return? Let's to 2.
my_top_n = 100

results = optimize(df=my_df,
                   parameters=my_parameters,
                   policies=my_policy,
                   filters=my_filters,
                   cost_function=my_cost_function,
                   top_n=my_top_n)

print(results)

# [(
#         origin destination   date_from     date_to  flight_price  stars  hotel_price  total_price  travelers  total_cost
# 0          NYC     Seattle  2024-01-10  2024-01-17         173.0    5.0       1387.0       1560.0          4     14304.0
# 1  Los Angeles     Seattle  2024-01-10  2024-01-17          61.0    4.0        217.0        278.0          8     14304.0
# 2      Chicago     Seattle  2024-01-10  2024-01-17          73.0    5.0       1387.0       1460.0          4     14304.0,
#   14304.0)]

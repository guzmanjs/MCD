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

import logging
import pandas as pd

from what_if.brute_force_general import optimize

# Step 1: Identify and prepate the data.
#
# We read the data from the original source. Here, the data set is "tidy",
# meaning that every combination of (Team Name, City) leads to a unique record.
# Note that the parameters choice means that the optimization routine will
# select *one city* to apply every records to. Having different parameters value
# for each of the records in the policy is a planned improvement.
my_df = (
    pd.read_csv("./data/sample_HC_data.csv")
)


my_parameters = ["City"]

# Step 2: Create the policy, filters, and cost function
#
# In our scenario, we have two "sub-teams" (one of 4, one of 8) that need to be
# onboarded.
my_policy = [
    {"Team Name": "Delta", "quantity": 4},
    {"Team Name": "Delta", "quantity": 8},
]

# In this example, we do not have any filters.
my_filters = {}


# The cost function needs to account for the capacity of the office.
def my_cost_function(df):
  # Summarize the data frames as needed. Every location has the same HQ Capacity
  # and utilized seats given a team
  answer = df.groupby(["City", "Team Name"]).agg({
      "Headquarter Capacity": 'min',
      "Utilized Seats": 'min',
      "REWS Cost": 'min',
      'quantity': 'sum'
  })
  logging.info(answer)
  if (answer['Headquarter Capacity'] >=
      (answer['Utilized Seats'] + answer["quantity"])).all():
    return (answer["quantity"] * answer["REWS Cost"]).sum()
  else:
    return float("inf")



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

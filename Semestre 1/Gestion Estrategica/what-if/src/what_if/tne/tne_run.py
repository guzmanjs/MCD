"""sample run for TnE previous Solution"""
import os
import json
import pandas as pd
from what_if.tne.scenario import Optimization
from what_if.tne.schema import Validation
from what_if.tne.cost_function import (estimate_flight_cost,
                                           estimate_hotel_cost)

DIR_SCENARIO_INPUT = "./src/what_if/tne/scenarios_combined"
INPUT_FILENAME="sample_scenario13_body.json"
INPUT_FILE_PATH = os.path.join(DIR_SCENARIO_INPUT, INPUT_FILENAME)
with open(INPUT_FILE_PATH, 'r',encoding="utf-8") as file:
        input_json = json.load(file)

history_data = pd.read_csv("./data/combined_flight_and_hotel_data.csv",index_col=False)
history_data["Date"] = pd.to_datetime(history_data['Date'], format="%Y-%m-%d")
cost_function_list =[estimate_hotel_cost,estimate_flight_cost]
results = Optimization(Validation(**input_json),history_data,cost_function_list).get_best_recommendations()
print(results)

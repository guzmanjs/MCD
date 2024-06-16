# _What-if?_ Scenario planner tool

## Description

This repository contains the code for the `what-if` package that allows users to optimize the decisions made on a dataset based on a TnE scenario. The library accomodates multiple data sets and scenarios.

1. **annealing_algorithm.py**
    Description: This module works on core logic of annealing algorithm. The annealing algorithm optimizes solutions by simulating the physical process of annealing. It starts with an initial solution, iterates through neighboring solutions while gradually decreasing randomness (controlled by temperature), and accepts solutions based on their minimal cost  and the current temperature. This process continues until a termination condition is met.

2. **genetic_algorithm.py**
    Description: The genetic algorithm (GA) is a heuristic optimization method inspired by the principles of natural selection and genetics. It repeatedly modifies a population of individual solutions to arrive at the best solution for the problem at hand. GA is particularly useful for optimization problems where the search space is vast and complex.

3. **tabu_search.py**
    Description: This module works on core logic of tabu search optimization. It takes 2 hyper parameters 1- no. of ieterations 2- no. of sample generations. In each iteration ,a random location is selected and based on it no. samples are generated and passed to the cost functions.Post all iterations, top 3 location are sorted out based on minimal overall cost.

4. **config.py**
    Description: script where have mentioned hyperparameters for each algorithms and multiprocessing args.

5. **cost_function.py**
    Description: This module includes all different cost functions which can be used for calculating oevrall cost.

6. **utilities.py**
    Description: Supply utilities functions like generating neighbouring dates and solutions,function to format response.

7. **scenario.py**
    Description: It contain a main object function where all the algorithms are called via multithreading process.
    Collecting results from all threads and return best three solution.

8. **schema.py**
    Description: Have used pydantic module to validate input arguments. 
    Its being validate while calling the Optimize function from scenario.py.

9. **tne_test.py**
    Description: This script contains testcases to check working functions in use from  above all files.

10. **tne_scenario_test.py**
    Description: This script tests the scenario-based optimization processes defined in the what_if package. It ensures that:
    The total cost calculated from optimization matches expected values for various scenarios.
    Dataframes returned by the optimization process are properly structured and contain the expected 'total_cost' column.
    The optimization function integrates all parts of the process, including data preparation, applying filters, and executing the optimization, to provide accurate results.


## Installation

- This library use [Poetry](https://python-poetry.org/) as a package management. 
 
- To use Go-Finv, follow these steps:
    - Clone the repository:
    ```
    git clone https://gitpct.epam.com/go2-finv/what-if.git
    ```
    - Navigate to the project directory:
    ```
    cd what_if
    ```
    - Install dependencies and set up the virtual environment with Poetry:
    ```
    poetry install
    ```
    - Activate the virtual environment created by Poetry:
    ```
    poetry shell
    ```
    - Build source files and grab the resulting wheel from the `dist/` directory:
    ```
    poetry build
    ```
    - evaluate pytest files:
    ```
    poetry run pytest 
    ```
    - Run the optimize to evaluate total_cost for any separate scenarios:
    ```
    poetry run python src\what_if\tne\tne_run.py
    ``` 

## Usage

The library uses [pdoc3](https://pdoc3.github.io/pdoc/) for public documentation. The documentation can be generated using `pdoc --html --output-dir html what-if`.

The primary function of the package is the `get_best_recommendations()` function,which is the instance method of class object `Optimization`, takes the following parameters.

`input_attr`: A pydantic Basemodel object with mandate and optional attributes. We can add attributes as per requriements. Please check th json_schema.json file to check on inputs required.

`data`: A pandas DataFrame which contains the information necessary for the optimization routine.

`cost_function`: a list of functions. Each function should be created as that it takes three input attributes `Trip` scenario trip basemodel object which is provided in the input attributes `data` the dataset on which the trip scenario would be used to filter records `response`  a dict which will be updated based on all different values user wants to get in overall response.



## Dataframe Description df for T&E spend
- File Name: "combined_flight_and_hotel_data.csv"

- General Description: This dataset combines flight and hotel booking data to facilitate comprehensive travel optimization scenarios. It is designed to support decision-making processes by providing critical travel details that can be analyzed and optimized according to various trips, list of potential destination, and other requried arguments.

**Key Features**
Scenario generation based on user input parameters (origin, travel dates, destination, etc.).
Calculation of total cost for each scenario with a breakdown by categories.
Comparison of potential savings across scenarios.
Optimization recommendations for T&E spend.

**Input Parameters for each Trip**
Origin : Origin location for the trip.
Travel Dates: The planned dates for travel.
Destination: The target location for travel.
Hotel Preferences: Accommodation preferences, including hotel stars and amenities.
Transportation Preferences: Preferences for modes of transport.
Other Expenses: Additional costs associated with travel.
Number of People: The total number of travelers.

**Optmization Goals**
Minimize Total Costs: Reduce the overall expenses associated with flights and hotels while considering inflation and other dynamic factors.
Adhere to input attributes for each trip: Respect given business limitations including travel dates, destinations, and the number of travelers.

### Columns and Descriptions:
- Column Name: origin
Description: The departure city or airport code for the flight.
Data Type: String
- Column Name: destination
Description: The arrival city or airport code for the flight.
Data Type: String
- Column Name: date_from
Description: The departure date for the flight.
Data Type: Date
- Column Name: date_to
Description: The return date for the flight.
Data Type: Date
- Column Name: price
Description: The total price for the flight and hotel package.
Data Type: Numeric
- Column Name: travelers
Description: The number of travelers for whom the booking is made.
Data Type: Integer
- Column Name: flight_number
Description: The flight number associated with the booking.
Data Type: String
- Column Name: hotel_rating
Description: The star rating of the hotel included in the booking.
Data Type: Numeric
- Column Name: amenities
Description: A list of amenities provided by the hotel.
Data Type: String
- Column Name: total_price
Description: The total price calculated based on the number of travelers and the price per package.
Data Type: Numeric

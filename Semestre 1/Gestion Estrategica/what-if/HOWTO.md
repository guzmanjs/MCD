# _What if?_ scenario planner tool: end-user guide

## Who is this for?

This document is for the user of the _what-if?_ scenario planning library. <!-- If you are developing the library, please follow the development guide that will follow -->.

## Pre-requisites

The dependencies should be resolvable during the installation steps. The library was tested with Python 3.12.

<!-- TODO: Note: do we want to relax the Python version requirements? -->

## Installation

_Placeholder for installation instructions from Piper._

### Local installation from source

Note: Use only if you want to install a local copy of the library.

**Step 1:** If you have the source code zipped, unzip the archive and extract it to a folder in your cloudtop machine.

**Step 2:** From a terminal, reach the directory where the zip file was extracted.

```bash
cd <directory where the zip file is extracted>
```

**Step 3:** Install [Poetry](https://python-poetry.org/), which is used for dependency management and isolation.

```bash
sudo apt install python3-poetry
```

**Step 4:** Run the `poetry install` command to install the `what-if` package and the dependencies.

Caution: At times, we have witnessed Poetry hanging or taking too long to resolve dependencies. If this is the case, press `Ctrl+C` to cancel the execution and run it again. Poetry will resume and pick only the packages not yet installed.

**Step 5:** Follow the sub-instructions based on your use-case (each of them are independent):

**Step 5a:** If you want to run a Python REPL and play with the library, run `poetry shell`.

**Step 5b:** If you want to test an sample optimization routine, execute any of the files in the `/demo` directory:

```bash
poetry run python demos/01-travel-and-expense-multiple-travelers.py
```

You can also use any of the demos as a base file to customize for your own use-case.


## Creating your own optimization routine

The _what-if?_ library provides a flexible model to optimize based on your scenario. We recommend to follow the steps outlined below to create an optimization procedure contextualized to your problem and data. All of the demos provided as part of the repository follow the same steps if you want to follow along.

### Identify and prepare your data

The `optimize()` routine takes data in a pandas DataFrame. We recommend giving friendly names to the columns as they'll be used during the creation of the parameters, filters, policy, and cost function. (For a deeper discussion around the concepts used in the _what-if?_ library, checkout the [README.md](./README.md) section "The mental model of the `optimize()` routine").

When reviewing the data frame, ensure that each combination of the parameter/policy space has a unique record. If not, the problematic records will be returned to you when running the optimization routine.

The `optimize()` routine will return the optimal combination of parameters for the given scenario, so create a list of the column names you want to return as part of the optimization exercise.

### Create the policy, the filters, and cost function

In order for the optimization to start, you need to provide a policy and a cost function. A policy is a set of records that represent the scenario you want to optimize. We represent every record in a policy via a dictionary where at least one key must match the data frame (if not, then there is no way for the routine to match the policy to the data and the optimization will fail with an error message).

As a way to speed up the computations, you can optionally provide "filters" which are values in the data frame that the `optimize()` routine need to only consider. As an example, you may want to only focus on a subset of the data, some particular dates for a trip or an event, etc. The `filter` function parameter takes a dictionary mapping a column name to a list of admissible values.

_Note: Check out the `what_if.param_utils` package for helper functions to simplify the creation of filters!_

The cost function is – as the name suggest – a function that takes a data frame representing a realized scenario and returns a cost (floating point number). Based on the scenario at hand, you can create a lambda function of a regular function as long at the signature is compatible with what the 
optimize() routine accepts (input: pd.DataFrame, output: float). The cost function will be used to
`establish the minimum cost of all the scenarios`. 

_Note: a realized scenario is a combination of parameters that fulfills the policy provided to the `optimize()` routine._

As part of the cost function, if you want to reject some realized scenarios because of some business rules, return a value of `float("inf")`. As an example of this:

``` python
def rews_optim(df):
    # We want to make sure that the value of `current_allocation` + `quantity` is not above `total_capacity`.
    if (df["total_capacity"] >= (df["current_allocation"] + df["quantity"])).all():
        return (df["quantity"] * df["employee_cost"]).sum()
    else:
        # If it is the case, we reject through returning `float("inf")`.
        return float("inf")
```

_Note: we plan on improving the usability of the library by allowing explicit constraints to be inputted separately from the cost function._ 



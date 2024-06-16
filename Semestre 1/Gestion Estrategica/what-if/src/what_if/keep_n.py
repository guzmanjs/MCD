#!/usr/bin/env python3

# Removing the module documentation pylint alert because the class contains all the information.
# pylint: disable=missing-module-docstring
# pylint: disable=bad-indentation

class KeepN:
  """This is a lightweight structure to keep the top N results (based on the lowest cost).

  We try to keep a tradeoff between memory usage and abusive sorting by
  accumulating all the results without doing anything and sorting/keeping the
  relevant results periodically.

  The container currently only accepts tuple of the following form. We compare
  on the `cost`.

  (results, cost)

  """

  def __init__(self, n: int):
    """Class initializer.

    Args:
        n: int, number of elements we wish to retrun when we call `reture_results()`.
    """

    if n <= 0:
        raise ValueError("The number of elements in the KeepN "
                          "structure should be a positive integer.")
    self.n = n
    self._n = n  # Utility counter which keeps track of how many elements we have
    self.container = []  # Container for the values.

  def _sort_and_clean(self):
    """Cleaning routine. Removes all but the best `n` results."""
    self.container.sort(key=lambda x: x[1])
    self.container = self.container[0 : self.n]
    self._n = self.n

  def add_item(self, item):
    """Adds an item to the structure"""
    if item[1] < float("inf") and item[1] not in [x[1] for x in self.container]:
      self.container.append(item)
      self._n += 1
    if self._n > self.n * 10000:
      self._sort_and_clean()
      print("Intermediate cleaning. Result set:")
      print(self.return_results())
      print("\n\n")

  def return_results(self):
    """Returns the top `n` results in a list."""
    self._sort_and_clean()
    return [x for x in self.container if x[1] < float("inf")]

#!/usr/bin/env python3

"""Test cases for KeepN data structure class."""

# pylint: disable=wildcard-import, missing-function-docstring,
# pylint: disable=redefined-outer-name, unused-wildcard-import
# pylint: disable=bad-indentation

import pytest

from what_if.keep_n import KeepN


def test_an_empty_collection_returns_empty():
  kn = KeepN(3)
  results = kn.return_results()
  assert results == []


def test_a_collection_with_only_infinites_should_return_empty():
  only_infinites = KeepN(3)
  for _ in range(10):
      only_infinites.add_item(({}, float("inf")))

  results = only_infinites.return_results()

  assert results == []


def test_adding_less_than_n_items_returns_all_of_them():
  less_than_three = KeepN(3)
  less_than_three.add_item(({}, 3))

  results = less_than_three.return_results()

  assert results == [({}, 3)]


def test_adding_more_than_n_items_returns_the_top_n():
  more_than_three = KeepN(3)
  for i in range(10, 1, -1):
    more_than_three.add_item(({}, i))

  results = more_than_three.return_results()

  assert results == [({}, 2), ({}, 3), ({}, 4)]


def test_negative_n_param_raise_value_error():
  with pytest.raises(ValueError) as exc_info:
        _ = KeepN(-1)

  assert exc_info.type is ValueError
  assert (
      exc_info.value.args[0] ==
      "The number of elements in the KeepN structure should be a positive integer."
  )

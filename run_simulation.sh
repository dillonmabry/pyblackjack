#!/bin/sh
for run in {1..10}; do
  python -m pyblackjack 1000000 4 0.75 basic_strategy >> basic_strat_output.txt
done

for run in {1..10}; do
  python -m pyblackjack 1000000 4 0.75 basic_strategy_alt >> basic_strat_alt_output.txt
done

for run in {1..10}; do
  python -m pyblackjack 1000000 4 0.75 simple >> simple_output.txt
done
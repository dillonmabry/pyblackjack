#!/bin/sh
# Basic strat
for run in {1..5}; do
  python -m pyblackjack 1000000 4 0.75 basic_strategy >> basic_strat_output_4_75.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 1 0.75 basic_strategy >> basic_strat_output_1_75.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 1 0.50 basic_strategy >> basic_strat_output_1_50.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 4 0.50 basic_strategy >> basic_strat_output_4_50.txt
done

# Alt strat
for run in {1..5}; do
  python -m pyblackjack 1000000 4 0.75 basic_strategy_alt >> basic_strat_alt_output_4_75.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 1 0.75 basic_strategy_alt >> basic_strat_alt_output_1_75.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 1 0.50 basic_strategy_alt >> basic_strat_alt_output_1_50.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 4 0.50 basic_strategy_alt >> basic_strat_alt_output_4_50.txt
done

# Simple strat
for run in {1..5}; do
  python -m pyblackjack 1000000 4 0.75 simple >> simple_output_4_75.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 1 0.75 simple >> simple_output_1_75.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 1 0.50 simple >> simple_output_1_50.txt
done

for run in {1..5}; do
  python -m pyblackjack 1000000 4 0.50 simple >> simple_output_4_50.txt
done
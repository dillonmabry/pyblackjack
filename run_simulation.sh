#!/bin/sh
# 4 decks 75 percent shuffle, 1 million game series
for run in {1..10}; do
  python -m pyblackjack 1000000 4 0.75 basic_strategy >> basic_strat_output_4_75.txt
done
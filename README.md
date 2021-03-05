# PyBlackjack
Extremely basic python Blackjack simulator

This will not run on Windows because Windows uses a different forking strategy for multiprocessing. Also Windows is terrible.

## Development Instructions

### Setup
```
python setup.py install
```

### Run
```
python -m pyblackjack 1 4 0.75 basic_strategy
```
Runs 1 simulation with 4 decks with 75% shuffle rate using basic_strategy

```
python -m pyblackjack <Num Sims> <Num Decks> <Shuffle perc> <Strategy>
```

#### Tests
```
pytest
```

"""Main module"""
import argparse
import math
import time
import multiprocessing
import logging
import sys
from .game import Game
from .deck import Deck
from .strategy import BasicStrategy, SimpleStrategy


def new_deck(num_decks):
    """Create new deck and shuffle
    Args:
        num_decks: number of decks to use for shuffle
    Returns shuffled deck
    """
    deck = Deck(num_decks)
    deck.shuffle()
    deck.cut()
    return deck


def get_strategy(strategy):
    """Generates player strategy to use based on input
    Args:
        strategy: user input strategy
    Returns strategy class
    """
    if strategy == "basic_strategy":
        return BasicStrategy(None)
    if strategy == "basic_strategy_alt":
        return BasicStrategy(None, strat_file="basic_strategy_alt")
    if strategy == "simple":
        return SimpleStrategy(None)


def simulate(queue, batch_size, num_decks, shuffle_perc, strategy):
    """Run single batch of simulations
    Args:
        batch_size: the batch size of games to run
        num_decks: number of decks to use
        shuffle_perc: at percentage used, reshuffle deck
        strategy: player strategy to use
    Adds results of sims to queue
    """
    deck = new_deck(num_decks)
    batch_info = {"ties": 0, "wins": 0,
                  "losses": 0, "earnings": 0, "num_hands": 0}
    for _ in range(0, batch_size):
        game = Game(deck, strategy)
        if (float(len(game.deck.cards)) / (52 * num_decks)) < shuffle_perc:  # re-shuffle new deck
            game.deck = new_deck(num_decks)
        game.play()
        batch_info["ties"] += game.game_info["ties"]
        batch_info["wins"] += game.game_info["wins"]
        batch_info["losses"] += game.game_info["losses"]
        batch_info["earnings"] += game.game_info["earnings"]
        batch_info["num_hands"] += (game.game_info["wins"] +
                                    game.game_info["losses"] + game.game_info["ties"])
    queue.put(batch_info)


def main():
    """Main method for cmd util"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "num_sims", type=int, help="Enter the number of simulations to run")
    parser.add_argument("num_decks", type=int,
                        help="Number of decks to use", choices=[1, 2, 3, 4])
    parser.add_argument("shuffle_perc", type=float,
                        help="Shuffle percentage", choices=[0.50, 0.75])
    parser.add_argument("strategy", type=str, help="Player strategy to use", choices=[
                        "basic_strategy", "basic_strategy_alt", "simple"])
    parser.add_argument('-d', action='store_true', help="Debug on/off")
    args = parser.parse_args()

    if args.d:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    if args.num_sims < 1:
        logging.error("Please enter number of simulations >= 1")
    elif args.num_sims == 1:
        deck = new_deck(args.num_decks)
        game = Game(deck, get_strategy(args.strategy))
        game.play()
        game.display_results()
        return
    else:
        start_time = time.time()
        cpus = multiprocessing.cpu_count()
        batch_size = int(math.ceil(args.num_sims / float(cpus)))
        queue = multiprocessing.Queue()

        processes = []
        for _ in range(0, cpus):
            process = multiprocessing.Process(
                target=simulate, args=(queue, batch_size,
                                       args.num_decks, args.shuffle_perc,
                                       get_strategy(args.strategy)))
            processes.append(process)
            process.start()

        for proc in processes:
            proc.join()

        finish_time = time.time() - start_time
        ties, wins, losses, num_hands, earnings = 0, 0, 0, 0, 0.0
        for _ in range(0, cpus):
            results = queue.get()
            wins += results["wins"]
            ties += results["ties"]
            losses += results["losses"]
            num_hands += results["num_hands"]
            earnings += results["earnings"]

        logging.info('Total simulations: %d', args.num_sims)
        logging.info('Simulations/s: %d', (float(args.num_sims) / finish_time))
        logging.info('Execution time: %.2fs', finish_time)
        logging.info('Hand win percentage: %.2f%%',
                     ((wins / float(num_hands)) * 100))
        logging.info('Hand draw percentage: %.2f%%',
                     ((ties / float(num_hands)) * 100))
        logging.info('Hand lose percentage: %.2f%%',
                     ((losses / float(num_hands)) * 100))
        logging.info('Total Earnings: %.2f', earnings)
        logging.info('Expected Earnings per game: %.2f',
                     (earnings / args.num_sims))
        logging.info('Expected Earnings per hand: %.2f\n',
                     (earnings / num_hands))


if __name__ == '__main__':
    main()

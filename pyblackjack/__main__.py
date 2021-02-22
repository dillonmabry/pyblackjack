import argparse
import math
import time
import multiprocessing
from .game import Game
from .deck import Deck
from .strategy import BasicStrategy, SimpleStrategy


def new_deck(num_decks):
    """Create new deck and shuffle
    Returns shuffled deck
    """
    deck = Deck(num_decks)
    deck.shuffle()
    deck.cut()
    return deck


def simulate(queue, batch_size, num_decks, shuffle_perc, strategy):
    """Run single batch of simulations
    Args:
        batch_size: the batch size of games to run for a particular single deck plus shuffle replacement
        num_decks: number of decks to use
        shuffle_perc: at percentage of cards used, will reshuffle the deck and cut
        strategy: player strategy to use
    Adds results of sims to queue
    """
    deck = new_deck(num_decks)
    game_info = {"ties": 0, "wins": 0,
                 "losses": 0, "earnings": 0, "num_hands": 0}
    for i in range(0, batch_size):
        game = Game(deck, strategy)
        if (float(len(game.deck.cards)) / (52 * num_decks)) < shuffle_perc:
            game.deck = new_deck(num_decks)
        game.play()
        game_info["ties"] += game.ties
        game_info["wins"] += game.wins
        game_info["losses"] += game.losses
        game_info["earnings"] += game.earnings
        game_info["num_hands"] += (game.ties + game.wins + game.losses)
    queue.put(game_info)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "num_sims", type=int, help="Enter the number of simulations to run")
    parser.add_argument("num_decks", type=int,
                        help="Number of decks to use", choices=[1, 2, 3, 4])
    parser.add_argument("shuffle_perc", type=float,
                        help="Shuffle percentage of when deck limit is reached, standard is 75%", choices=[0.50, 0.75])
    args = parser.parse_args()

    if args.num_sims < 1:
        print("Please enter number of simulations >= 1")
    elif args.num_sims == 1:
        deck = new_deck(args.num_decks)
        game = Game(deck, BasicStrategy([]))
        game.play()
        game.display_results()
        return
    else:
        start_time = time.time()
        cpus = multiprocessing.cpu_count()
        batch_size = int(math.ceil(args.num_sims / float(cpus)))
        queue = multiprocessing.Queue()

        processes = []
        for i in range(0, cpus):
            process = multiprocessing.Process(
                target=simulate, args=(queue, batch_size, args.num_decks, args.shuffle_perc, BasicStrategy([])))
            processes.append(process)
            process.start()

        for proc in processes:
            proc.join()

        finish_time = time.time() - start_time
        ties, wins, losses, num_hands, earnings = 0, 0, 0, 0, 0.0
        for i in range(0, cpus):
            results = queue.get()
            wins += results["wins"]
            ties += results["ties"]
            losses += results["losses"]
            num_hands += results["num_hands"]
            earnings += results["earnings"]

        print('Total simulations: %d' % args.num_sims)
        print('Simulations/s: %d' % (float(args.num_sims) / finish_time))
        print('Execution time: %.2fs' % finish_time)
        print('Hand win percentage: %.2f%%' %
              ((wins / float(num_hands)) * 100))
        print('Hand draw percentage: %.2f%%' %
              ((ties / float(num_hands)) * 100))
        print('Hand lose percentage: %.2f%%' %
              ((losses / float(num_hands)) * 100))
        print('Total Earnings: %.2f' % earnings)
        print('Expected Earnings per game: %.2f' % (earnings / args.num_sims))


if __name__ == '__main__':
    main()

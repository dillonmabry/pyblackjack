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
    tie, win, loss = 0, 0, 0
    for i in range(0, batch_size):
        game = Game(deck, strategy, 1000)
        if (float(len(game.deck.cards)) / (52 * num_decks)) < shuffle_perc:
            game.deck = new_deck(num_decks)
        result = game.play()
        if result == 0:
            tie += 1
        if result == 1:
            win += 1
        if result == 2:
            loss += 1
    queue.put([win, tie, loss])


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
        game = Game(deck, SimpleStrategy([]), 1000)
        result = game.play()
        game.display_results(result)
        return
    else:
        start_time = time.time()
        cpus = multiprocessing.cpu_count()
        batch_size = int(math.ceil(args.num_sims / float(cpus)))
        queue = multiprocessing.Queue()

        processes = []
        for i in range(0, cpus):
            process = multiprocessing.Process(
                target=simulate, args=(queue, batch_size, args.num_decks, args.shuffle_perc, SimpleStrategy([])))
            processes.append(process)
            process.start()

        for proc in processes:
            proc.join()

        finish_time = time.time() - start_time
        tie, win, loss = 0, 0, 0
        for i in range(0, cpus):
            results = queue.get()
            win += results[0]
            tie += results[1]
            loss += results[2]

        print('Total simulations: %d' % args.num_sims)
        print('Simulations/s: %d' % (float(args.num_sims) / finish_time))
        print('Execution time: %.2fs' % finish_time)
        print('Win percentage: %.2f%%' % ((win / float(args.num_sims)) * 100))
        print('Draw percentage: %.2f%%' % ((tie / float(args.num_sims)) * 100))
        print('Lose percentage: %.2f%%' %
              ((loss / float(args.num_sims)) * 100))


if __name__ == '__main__':
    main()

import argparse
import math
import time
import multiprocessing
from .game import Game
from .strategy import BasicStrategy, SimpleStrategy


def simulate(num_decks, shuffle_perc, queue, num_sims):
    tie, win, loss = 0, 0, 0
    for i in range(0, num_sims):
        game = Game(num_decks, shuffle_perc, SimpleStrategy([]))
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
    parser.add_argument("num_decks", type=int, help="Number of decks to use")
    parser.add_argument("shuffle_perc", type=float,
                        help="Shuffle percentage of when deck limit is reached, standard is 75%")
    args = parser.parse_args()

    start_time = time.time()

    cpus = multiprocessing.cpu_count()
    batch_size = int(math.ceil(args.num_sims / float(cpus)))
    queue = multiprocessing.Queue()

    processes = []
    for i in range(0, cpus):
        process = multiprocessing.Process(
            target=simulate, args=(args.num_decks, args.shuffle_perc, queue, batch_size))
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

    print('  cores used: %d' % cpus)
    print('  total simulations: %d' % args.num_sims)
    print('  simulations/s: %d' % (float(args.num_sims) / finish_time))
    print('  execution time: %.2fs' % finish_time)
    print('  win percentage: %.2f%%' % ((win / float(args.num_sims)) * 100))
    print('  draw percentage: %.2f%%' % ((tie / float(args.num_sims)) * 100))
    print('  lose percentage: %.2f%%' % ((loss / float(args.num_sims)) * 100))


if __name__ == '__main__':
    main()

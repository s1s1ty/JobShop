from .helper import *

import math
import random
import time


class SimulatedAnnealing(object):
    def __init__(self):
        pass

    def __random_schedule(self, j, m):
        schedule = [i for i in list(range(j)) for _ in range(m)]
        random.shuffle(schedule)

        return schedule

    def __cost(self, jobs, schedule):
        j = len(jobs)
        m = len(jobs[0])

        tj = [0]*j
        tm = [0]*m

        ij = [0]*j

        for i in schedule:
            machine, time = jobs[i][ij[i]]
            ij[i] += 1

            start = max(tj[i], tm[machine])
            end = start + time
            tj[i] = end
            tm[machine] = end

        return max(tm)

    def __get_neigbors(self, state, mode="normal"):
        neighbors = []

        for i in range(len(state)-1):
            n = state[:]
            if mode == "normal":
                swap_index = i + 1
            elif mode == "random":
                swap_index = random.randrange(len(state))

            n[i], n[swap_index] = n[swap_index], n[i]
            neighbors.append(n)

        return neighbors


    def __simulated_annealing(self, jobs, T, termination, halting, mode, decrease):
        total_jobs = len(jobs)
        total_machines = len(jobs[0])

        state = self.__random_schedule(total_jobs, total_machines)

        for i in range(halting):
            T = decrease * float(T)

            for k in range(termination):
                actual_cost = self.__cost(jobs, state)

                for n in self.__get_neigbors(state, mode):
                    n_cost = self.__cost(jobs, n)
                    if n_cost < actual_cost:
                        state = n
                        actual_cost = n_cost
                    else:
                        probability = math.exp(-n_cost/T)
                        if random.random() < probability:
                            state = n
                            actual_cost = n_cost

        return actual_cost, state

    def simulated_annealing_search(self, jobs, max_time=None, T=200, termination=10, halting=10, mode="random", decrease=0.8):
        num_experiments = 1

        solutions = []
        best = 10000000

        t0 = time.time()
        total_experiments = 0

        j = len(jobs)
        m = len(jobs[0])
        rs = self.__random_schedule(j, m)

        while True:
            try:
                start = time.time()

                for i in range(num_experiments):
                    cost, schedule = self.__simulated_annealing(jobs, T=T, termination=termination, halting=halting, mode=mode, decrease=decrease)

                    if cost < best:
                        best = cost
                        solutions.append((cost, schedule))

                total_experiments += num_experiments

                if max_time and time.time() - t0 > max_time:
                    raise TimeExceed("Time is over")

                t = time.time() - start
                if t > 0:
                    print("Best:", best, "({:.1f} Experiments/s, {:.1f} s)".format(
                            num_experiments/t, time.time() - t0))

                if t > 4:
                    num_experiments //= 2
                    num_experiments = max(num_experiments, 1)
                elif t < 1.5:
                    num_experiments *= 2

            except (KeyboardInterrupt, TimeExceed) as e:
                print()
                print("================================================")
                print("Best solution:")
                print(solutions[-1][1])
                print("Found in {:} experiments in {:.1f}s".format(total_experiments, time.time() - t0))

                return solutions[-1]


import random

def random_schedule(j, m):
    schedule = [i for i in list(range(j)) for _ in range(m)]
    random.shuffle(schedule)

    return schedule


def cost(jobs, schedule):
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


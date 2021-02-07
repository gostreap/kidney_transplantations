from random import randint, sample


def loadtxt(path):
    """
    Return the number of vertices n, the threshold K and the adkacency matrix of the directed graph M.
    """
    file = open(path, "r")
    lines = file.readlines()

    n = int(float(lines[0].strip()))
    K = float(lines[1].strip())
    M = []
    for i in range(n):
        M.append([])
        M[i] = list(map(int, map(float, lines[i + 2].strip().split("   "))))

    return n, K, M


def matrix_to_adjacency_list(M):
    lists = []
    for i, row in enumerate(M):
        lists.append([])
        for j, c in enumerate(row):
            if c == 1:
                lists[i].append(j)
    return lists

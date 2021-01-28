from random import randint, sample
from igraph import Graph


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
        M[i] = list(map(float, lines[i + 2].strip().split("   ")))

    return n, K, M


def generate_data(n):
    """
    Return the number of donor-patient pairs n, an array of set of compatible kidneys K, \
    an array of preference list P and an priority list of the patient U.
    """
    rg = list(range(n))
    K = []
    P = []
    U = sample(rg, len(rg))

    for i in range(n):
        list_of_kidneys = sample(rg, randint(1, n))
        K.append(set(list_of_kidneys))
        if i in K[i]:
            P.append(sample(list_of_kidneys + ["w"], len(list_of_kidneys) + 1))
            id_i = P[i].index(i)
            P[i][0], P[i][id_i] = P[i][id_i], P[i][0]
        else:
            P.append(sample(list_of_kidneys + [i, "w"], len(list_of_kidneys) + 2))
    return n, K, P, U


def get_graph_from_K(n, K):
    """
    Return a graph as defined in 3.2
    """
    g = Graph()
    g.layout("sphere")
    g.add_vertices(n)

    for i in range(n):
        g.vs[i]["label"] = str(i)

    for i in range(n):
        for j in K[i]:
            if i in K[j]:
                g.add_edges([(i, j)])

    return g


def matrix_to_adjacency_list(M):
    lists = []
    for i, row in enumerate(M):
        lists.append([])
        for j, c in enumerate(row):
            if c == 1:
                lists[i].append(j)
    return lists

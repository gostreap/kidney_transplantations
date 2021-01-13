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
        P.append(sample(list_of_kidneys+["w"], len(list_of_kidneys) + 1))

    return n, K, P, U
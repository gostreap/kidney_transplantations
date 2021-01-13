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
        M[i] = list(map(float, lines[i+2].strip().split("   ")))

    return n, K, M

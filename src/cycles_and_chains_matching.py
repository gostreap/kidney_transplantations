from igraph import plot

def greedy_matching(n, K, P, U):
    c, w = [], []

    # The graph is a reverse directed Tree
    preffered_kidneys = [P[i][0] for i in range(n)]
    tree = [[] for i in range(n)]
    matched = [False for i in range(n)]

    for i in range(n + 1):
        j = preffered_kidneys[i]
        if j = "w":
            tree[n+1].append(i)
        else:
            tree(j).append(i)
    assigned_kidneys = [False for i in range(n)]
    
    g = get_graph_from_tree(tree)
    plot(g)



    return c, w

def detect_cycle(tree):
    pass

def select_chain_A(preffered_kidneys, U):
    pass

def select_chain_B(preffered_kidneys, U):
    pass

def update_graph(matched):
    preffered_kidneys = []

def run_random(n):
    n, K, P, U = generate_data(n)
    # print(U)
    # for i in range(n):
    #     print(i, "->", K[i], "-", P[i])
    # g = get_graph_from_tree(n, K)
    # c, w = greedy_matching(n, K, P, U)

    # for i, j in c:
    #     print(i, j)
    #     g.es[g.get_eid(i, j)]["color"] = "red"
    # plot(g)
    return greedy_matching(n, K, P, U)


def get_graph_from_tree(tree):
    """
    Return a graph as defined in 3.2
    """
    g = Graph()
    # g.layout("sphere")
    g.add_vertices(n+1)

    for i in range(n):
        g.vs[i]["label"] = str(i)
    g.vs(n)["label"] = "w"

    for i in range(n+1):
        for j in tree[i]:
            g.add_edges([(i, j)])

    return g
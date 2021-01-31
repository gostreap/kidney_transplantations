from utils import generate_data, get_graph_from_K
from jgraph import plot


def greedy_matching(n, K, P, U):
    c, w = [], []
    matched = [False for i in range(n)]
    # We run through the priority list of the patient and give them their best choice.
    for i in U:
        if matched[i]:
            continue
        for j in P[i]:
            if j == "w":
                w.append(i)
                matched[i] = True
                break
            elif not matched[j] and i in K[j]:
                c.append((i, j))
                matched[i] = matched[j] = True
                break

    return c, w


def run_random(n):
    n, K, P, U = generate_data(n)
    print(U)
    for i in range(n):
        print(i, "->", K[i], "-", P[i])
    g = get_graph_from_K(n, K)
    c, w = greedy_matching(n, K, P, U)

    for i, j in c:
        print(i, j)
        g.es[g.get_eid(i, j)]["color"] = "red"
    plot(g)
    return greedy_matching(n, K, P, U)


c, w = run_random(5)
print("c ->", c)
print("w ->", w)

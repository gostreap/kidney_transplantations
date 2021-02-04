def greedy_matching(n, K, P, U, is_matched=None):
    M = []
    if is_matched is None:
        is_matched = [False for i in range(n)]
    sorted_K = []

    for i in range(n):
        sorted_K.append(list(K[i]))
        sorted_K[i].sort(key=lambda x: P[i][x], reverse=True)

    for u in U:
        if not is_matched[u]:
            for v in sorted_K[u]:
                if not is_matched[v]:
                    if P[v][u] >= P[v][v] and P[v][u] >= P[v][n]:
                        M.append((u, v))
                        is_matched[u] = True
                        is_matched[v] = True
                        break

    return M

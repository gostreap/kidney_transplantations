def construct_cycle(next_vertices, start):
    cycle = [start]
    while next_vertices[cycle[-1]] != start:
        cycle.append(next_vertices[cycle[-1]])
    return cycle


def detect_cycle(next_vertices, removed):
    n = len(next_vertices)
    seen = set()
    cycles = []
    for i in range(len(next_vertices)):
        if i in seen or i in removed:
            continue
        current_path = {i}
        is_cycle = True
        while next_vertices[i] not in current_path:
            # If the next vertices is w then the current chain is not a cycle
            if next_vertices[i] == n or next_vertices[i] in seen or next_vertices[i] in removed:
                is_cycle = False
                break

            i = next_vertices[i]
            current_path.add(i)

        # i is in a cycle
        if is_cycle:
            # print("cycle", i, current_path)
            cycles.append(construct_cycle(next_vertices, i))
        seen = seen | current_path
    return cycles


def get_depth(tree, s, depth):
    for i in tree[s]:
        depth[i] = depth[s] + 1
        depth = get_depth(tree, i, depth)
    return depth


def get_heads(depth, removed, is_matched):
    # print(depth)
    heads = []
    max_depth = 0
    for i, d in enumerate(depth):
        if i < len(depth) - 1 and (i in removed or is_matched[i]):
            continue
        if d > max_depth:
            heads = [i]
            max_depth = d
        elif d == max_depth:
            heads.append(i)
    return heads


def get_chains(next_vertices, heads):
    chains = []
    for head in heads:
        chain = []
        current = head
        n = len(next_vertices)
        while current != n:
            chain.append(current)
            current = next_vertices[current]
        chains.append(chain)
    return chains


def reverse_next_vertices(next_vertices, removed):
    n = len(next_vertices)
    reverse = [[] for i in range(n + 1)]
    for i in range(n):
        reverse[next_vertices[i]].append(i)
    return reverse


def select_chain_A(next_vertices, removed, is_matched, U):
    n = len(next_vertices)
    reverse_adjacency_lists = reverse_next_vertices(next_vertices, removed)
    depth = [-1 for i in range(n + 1)]
    depth[n] = 0
    depth = get_depth(reverse_adjacency_lists, n, depth)

    # print(depth)

    heads = get_heads(depth, removed, is_matched)
    
    # print(heads)

    chains = get_chains(next_vertices, heads)
    
    # print(chains)

    if len(chains) == 1:
        return chains[0]

    vertices_in_chains = set()
    for chain in chains:
        vertices_in_chains = vertices_in_chains | set(chain)
    pos_in_U = [-1 for i in range(n)]
    for i, u in enumerate(U):
        pos_in_U[u] = i
    vertices_in_chains = list(vertices_in_chains)
    vertices_in_chains.sort(key=lambda x: pos_in_U[x], reverse=True)
    # chains_set = [set(chain) for chain in chains]
    best_chains = [i for i in range(len(chains))]

    for v in vertices_in_chains:
        # print(chains)
        # print(best_chains)
        v_in = []
        for i, chain in enumerate(chains):
            if v in chain:
                v_in.append(i)
        if len(v_in) != 0:
            chains = [chains[i] for i in v_in]
        if len(chains) == 1:
            return chains[0]


def select_chain_B(next_vertices, U):
    pass


def update_graph(next_vertices, is_matched, removed, sorted_K):
    n = len(is_matched)
    for i in range(n):
        if i in removed or is_matched[i]:
            continue
        find = False
        while not find:
            if sorted_K[i][-1] == n:
                next_vertices[i] = n
                find = True
            elif sorted_K[i][-1] in removed:
                del sorted_K[i][-1]
            else:
                next_vertices[i] = sorted_K[i][-1]
                find = True
    return next_vertices


def cycles_and_chains_matching(n, K, P, U, is_matched=None):
    M = []
    n_matched = n
    if is_matched is None:
        is_matched = [False for i in range(n)]
    sorted_K = []
    removed = set()

    for i in range(n):
        sorted_K.append(list(K[i]))
        sorted_K[i].append(n)
        sorted_K[i].sort(key=lambda x: P[i][x])
        # print("P", i, P[i])
        # print("sorted_K", i, sorted_K[i])

    next_vertices = [0 for i in range(n)]
    while n_matched != 0:
        # print(n_matched)
        # print("graph")
        next_vertices = update_graph(next_vertices, is_matched, removed, sorted_K)
        # print(next_vertices)
        # print("after graph")
        cycles = detect_cycle(next_vertices, removed)
        if len(cycles) != 0:
            # print("cycle")
            # print(cycles)
            for cycle in cycles:
                n_matched -= len(cycle)
                for i in range(len(cycle) - 1):
                    M.append((cycle[i], cycle[i + 1]))
                    is_matched[cycle[i]] = True
                    removed.add(cycle[i])
                M.append((cycle[-1], cycle[0]))
                is_matched[cycle[-1]] = True
                removed.add(cycle[-1])
        else:
            # print("before")
            # print(removed)
            # print(is_matched)
            chain = select_chain_A(next_vertices, removed, is_matched, U)
            if len(chain) == 0:
                break
            # print("after")
            n_matched -= len(chain)
            for i in range(len(chain) - 1):
                M.append((chain[i], chain[i + 1]))
                is_matched[chain[i]] = True
                removed.add(chain[i+1])
            is_matched[chain[-1]] = True

    # print(M)
    return M

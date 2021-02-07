class Node:
    
    def __init__(self, id, n, K, P):
        self.id = id
        self.n = n # size of the graph but also id of w
        self.K = K
        self.P = P
        self.sorted_K = list(K)
        self.sorted_K.append(self.n)
        self.sorted_K.sort(key=lambda x: P[x])
        self.assigned = False
        self.next = None
        self.previous = []

    def set_next(self, nodes, removed, unavailable):
        if self.assigned:
            return
        self.next = None
        while self.next is None:
            if self.sorted_K[-1] == self.n:
                self.next = self.n
            elif nodes[self.sorted_K[-1]] in removed or nodes[self.sorted_K[-1]] in unavailable:
                del self.sorted_K[-1]
            else:
                self.next = nodes[self.sorted_K[-1]]

    def get_depth(self, depth):
        for node in self.previous:
            depth[node.id] = depth[self.id] + 1
            depth = node.get_depth(depth)
        return depth

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return False
        return self.id == other.id

    def __str__(self):
        return "n" + str(self.id)

    def __repr__(self):
        return self.__str__()

class Graph:
    
    def __init__(self, n, K, P, U, is_matched=None):
        self.n = n
        self.K = K
        self.P = P
        self.U = U
        self.removed = set()
        self.passive = set()
        self.unavailable = set()
        self.nodes = []
        for id in range(n):
            self.nodes.append(Node(id, n, K[id], P[id]))
            if is_matched is not None and is_matched[id]:
                self.removed.add(self.nodes[id])
                
        self.pos_in_U = [-1 for i in range(n)]
        for i, u in enumerate(U):
            self.pos_in_U[u] = i

    def set_previous(self):
        for node in self.nodes:
            node.previous = []
        for node in self.nodes:
            if node.next != None and node.next != self.n:
                node.next.previous.append(node)

    def update(self):
        for node in set(self.nodes) - (self.removed | self.passive):
            node.set_next(self.nodes, self.removed, self.unavailable)
        self.set_previous()

    def assign_cycle(self, cycle):
        for node in cycle:
            node.assigned = True
            self.removed.add(node)

    def assign_chain(self, chain):
        for i, node in enumerate(chain):
            node.assigned = True
            self.passive.add(node)
            if i!= 0:
                self.unavailable.add(node)

    def get_cycle(self, start):
        cycle = [start]
        while cycle[-1].next != start:
            cycle.append(cycle[-1].next)
        return cycle

    def get_cycles(self):
        cycles = []
        marked = self.removed.copy()
        for node in set(self.nodes) - (self.removed | self.passive):
            if node in marked:
                continue
            path = set()
            while node not in marked and node != self.n:
                if node in path:
                    cycles.append(self.get_cycle(node))
                    break
                path.add(node)
                node = node.next
            marked = marked | path
        return cycles

    def get_depth(self):
        depth = [-1 for _ in range(self.n)]
        for node in self.nodes:
            if node.next == self.n:
                depth[node.id] = 1
                depth = node.get_depth(depth)
        return depth

    def get_heads(self):
        depth = self.get_depth()
        # print(depth)
        # depth_print = depth.copy()
        # for i in range(self.n):
        #     if self.nodes[i] in self.removed or self.nodes[i] in self.passive:
        #         depth_print[i] = -1
        # print(depth_print)
        heads = []
        max_depth = 0
        for i, d in enumerate(depth):
            if self.nodes[i] in self.removed or self.nodes[i] in self.passive:
                continue
            if d > max_depth:
                heads = [self.nodes[i]]
                max_depth = d
            elif d == max_depth:
                heads.append(self.nodes[i])
        # print("heads", heads)
        return heads

    def get_longest_chains(self):
        heads = self.get_heads()
        chains = []
        for head in heads:
            chain = []
            current = head
            while current != self.n:
                chain.append(current)
                current = current.next
            chains.append(chain)
        # print("chains", chains)
        return chains

    def select_chain_A(self):
        chains = self.get_longest_chains()
        nodes_in_chains = set()
        for chain in chains:
            nodes_in_chains = nodes_in_chains | set(chain)
        nodes_in_chains = list(nodes_in_chains)
        nodes_in_chains.sort(key=lambda x: self.pos_in_U[x.id])

        n_selectable = len(chains)
        selectable = [True for chain in chains]
        chains_set = [set(chain) for chain in chains]
        for node in nodes_in_chains:
            n_selectable = 0
            selectable_loop = []
            for i, chain in enumerate(chains):
                if not selectable[i]:
                    selectable_loop.append(False)
                elif node not in chains_set[i]:
                    selectable_loop.append(False)
                else:
                    selectable_loop.append(True)
                    n_selectable += 1
            if n_selectable == 1:
                for i, chain in enumerate(chains):
                    if selectable_loop[i]:
                        return chain
            elif n_selectable > 1:
                selectable = selectable_loop

    def is_every_nodes_assigned(self):
        return len(self.removed | self.passive) == self.n

    def get_assignement(self):
        assignement = []
        for node in self.nodes:
            if node.assigned and node.next != self.n:
                assignement.append((node.id, node.next.id))
        return assignement

    def __str__(self):
        s = ""
        for node in self.nodes:
            s += str(node) + "->" + str(node.next) + ":" + str(node.previous) + "\n"
        return s 

def cycles_and_chains_matching(n, K, P, U, is_matched=None):

    g = Graph(n, K, P, U, is_matched=is_matched)
    g.update()
    # i = 0
    while not g.is_every_nodes_assigned():
        # print(i, len(g.removed | g.passive))
        # i+=1
        g.update()
        cycles = g.get_cycles()
        if len(cycles) != 0:
            for cycle in cycles:
                g.assign_cycle(cycle)
        else:
            chain = g.select_chain_A()
            # print(chain)
            g.assign_chain(chain)
    return g.get_assignement()

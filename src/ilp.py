from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from utils import loadtxt, matrix_to_adjacency_list
from minimal_infeasible_paths import minimal_infeasible_path
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph 
import numpy as np
import matplotlib.pyplot as plt


def get_variables(n):
    A = []
    for i in range(n):
        A.append([])
        for j in range(n):
            A[i].append(LpVariable(name="x_{}_{}".format(i,j), lowBound=0, upBound=1, cat='Binary'))
    return A


def get_obj_func(A):
    sums = []
    for i in range(len(A)):
        sums.append(lpSum(A[i]))
    return lpSum(sums)


def get_constraints(A, k, M, min_paths):
    C = []

    for i in range(len(A)):
        for j in range(len(A)):
            C.append(A[i][j] <= M[i][j])

    for j in range(len(A)):
        vars_ij = []
        vars_ji = []
        for i in range(len(A)):
            vars_ij += A[i][j]
            vars_ji += A[j][i]
        C.append(lpSum(vars_ij) <= 1)
        C.append(lpSum(vars_ji) <= lpSum(vars_ij))

    for path in min_paths:
        vars = []
        for i in range(int(k)):
            vars.append(A[path[i]][path[i+1]])
        C.append(lpSum(vars) <= k-1)
    
    return C


    
def solve(n, k, M):
    adjacency_lists = matrix_to_adjacency_list(M)
    min_paths = minimal_infeasible_path(adjacency_lists, k)

    A = get_variables(n)
    obj_func = get_obj_func(A)
    C = get_constraints(A, k, M, min_paths)

    model = LpProblem(name="small-problem", sense=LpMaximize)
    model += obj_func
    
    for constraint in C:
        model += constraint

    status = model.solve()

    print(f"objective: {model.objective.value()}")

    for var in model.variables():
        if var.value() > 0.01:
            print(f"{var.name}: {var.value()}")

    g = nx.from_numpy_matrix(np.array(M), create_using=nx.DiGraph)
    pos = nx.circular_layout(g)

    for u,v in g.edges():
        g[u][v]['label'] = A[u][v].value()
        if A[u][v].value() > 0.001:
            g[u][v]['color']='red'
        else:
            g[u][v]['color']='black'
    # nx.draw(g, pos, edge_color=colors, with_labels=True)
    G = to_agraph(g) 
    G.layout('dot')                                                                 
    G.draw("multi.png")

def solve_file(file):
    n, k, M = loadtxt(file)
    solve(n, k, M)

    




solve_file("dataset/data1.txt")

# n = 3
# k = 2
# M = np.random.randint(2,size=(n,n))

# print(M)

# solve(n, k, M)

# g = nx.from_numpy_matrix(np.array(M), create_using=nx.DiGraph)
# print(g.edges())

# pos = nx.circular_layout(g)

# edges = g.edges()
# colors = ['r' if A[u][v].value() > 0.99 else 'w' for u,v in edges]
# edges = [(u,v) if A[u][v].value() > 0.99 else None for u,v in edges]

# edgelist = []
# for u,v in edges:
#     if A[u][v].value() > 0.99:
#         edgelist.append((u,v))
#         g[u][v]['color']='red'
#     else:
#         g[u][v]['color']='white'

# print(edgelist)

# nx.draw(g, pos, edge_color=colors, with_labels=True)
# nx.draw_networkx_nodes(g, pos)
# nx.draw_networkx_labels(g, pos)
# nx.draw_networkx_edges(g, pos, edgelist=edgelist)

# A = to_agraph(g) 
# A.layout('dot')                                                                 
# A.draw('multi.png')   

# nx.draw(g, with_labels=True)
# plt.show()
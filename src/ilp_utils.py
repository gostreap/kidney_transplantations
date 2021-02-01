import numpy as np
import os
import networkx as nx

from ilp import get_variables, get_obj_func, get_constraints, get_solution, is_integer_solution, solve, solve_file
from minimal_infeasible_paths import minimal_infeasible_path
from networkx.drawing.nx_agraph import to_agraph
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from utils import loadtxt, matrix_to_adjacency_list


def pulp_solve(n, k, M):
    adjacency_lists = matrix_to_adjacency_list(M)
    min_paths = minimal_infeasible_path(adjacency_lists, k)

    A = get_variables(n, 'Binary')
    obj_func = get_obj_func(A)
    C = get_constraints(A, k, M, min_paths)

    model = LpProblem(name="Kidney Exchange", sense=LpMaximize)
    model += obj_func
    for c in C:
        model += c
    status = model.solve()

    return round(model.objective.value()), get_solution(A)


def pulp_solve_file(file):
    n, k, M = loadtxt(file)
    return pulp_solve(n, k, M)


def is_problem_solution_integer(n, k, M):
    adjacency_lists = matrix_to_adjacency_list(M)
    min_paths = minimal_infeasible_path(adjacency_lists, k)

    A = get_variables(n, 'Continuous')
    obj_func = get_obj_func(A)
    C = get_constraints(A, k, M, min_paths)

    model = LpProblem(name="Kidney Exchange", sense=LpMaximize)
    model += obj_func
    for c in C:
        model += c
    status = model.solve()

    return is_integer_solution(model)


def write_problem(file, n, k, M):
    f = open(file, "w")
    f.write("   {:.7e}\n".format(n))
    f.write("   {:.7e}\n".format(k))
    for i in range(len(M)):
        for j in range(len(M)):
            f.write("   {:.7e}".format(M[i][j]))
        f.write("\n")


def write_solution(file, solution):
    f = open(file, "w")
    for i in range(len(solution)):
        for j in range(len(solution)):
            f.write("   {}".format(solution[i][j]))
        f.write("\n")


def write_solution_png(M, solution, file="graph.png"):
    g = nx.from_numpy_matrix(np.array(M), create_using=nx.DiGraph)

    for u,v in g.edges():
        if solution[u][v] == 1:
            g[u][v]['color']='red'
        else:
            g[u][v]['color']='black'

    G = to_agraph(g) 
    G.layout('dot')                                                                 
    G.draw(file)


def generate_problem(n, k, n_dataset):
    """
    Generates problems for which the optimal solution in linear programming is not only integer.
    """
    i = 0
    while i != n_dataset:
        M = np.random.randint(2, size=(n,n))
        if not is_problem_solution_integer(n, k, M):
            i += 1
            write_problem("dataset/non_integer_lp_solution_{}_{}_number_{}".format(n, k, i), n, k, M)


def solve_and_write_solution(file, file_sol):
    n, k, M = loadtxt(file)
    best, solution = solve(n, k, M)
    write_solution(file_sol, solution)
    write_solution_png(M, solution, file=file_sol + ".png")


def test_solve_file(file):
    best1, _ = pulp_solve_file(file)
    best2, _ = solve_file(file)
    return round(best1) == round(best2)


def test_solve():
    res = []
    for file in os.listdir("dataset/"):
        if file.startswith("non_integer_lp_solution_5"):
            res.append(test_solve_file("dataset/" + file))
    print("Correct :", res.count(True), "- Incorrect :", res.count(False))

solve_and_write_solution("dataset/test2.txt", "solution/test2")
solve_and_write_solution("dataset/test3.txt", "solution/test3")

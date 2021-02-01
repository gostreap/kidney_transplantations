import numpy as np

from ilp import get_variables, get_obj_func, get_constraints, get_solution, is_integer_solution
from minimal_infeasible_paths import minimal_infeasible_path
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
    pulp_solve(n, k, M)


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


def generate_problem(n, k, n_dataset):
    i = 0
    while i != n_dataset:
        M = np.random.randint(2, size=(n,n))
        if not is_problem_solution_integer(n, k, M):
            i += 1
            write_problem("dataset/non_integer_lp_solution_{}_{}_number_{}".format(n, k, i), n, k, M)


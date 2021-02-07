import numpy as np

from minimal_infeasible_paths import minimal_infeasible_path
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from random import sample
from utils import loadtxt, matrix_to_adjacency_list


def get_variables(n, cat):
    A = []
    for i in range(n):
        A.append([])
        for j in range(n):
            A[i].append(LpVariable(name="x_{}_{}".format(i,j), lowBound=0, upBound=1, cat=cat))
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


def is_integer_solution(model):
    for var in model.variables():
        if abs(var.value() - int(var.value())) > 0.001:
            return False
    return True


def get_solution(A):
    sol = []
    for i in range(len(A)):
        sol.append([])
        for j in range(len(A)):
            sol[i].append(round(A[i][j].value()))
    return sol


def branch_and_bound(A, obj_func, C, relaxed_var, best, solution):
    model = LpProblem(name="small-problem", sense=LpMaximize)
    model += obj_func
    for c in C:
        model += c

    status = model.solve()
    if status == -1:
        # problem is infeasible
        return best, solution
    elif model.objective.value() < best:
        return best, solution
    elif is_integer_solution(model):
        return model.objective.value(), get_solution(A)
    else:
        x = sample(relaxed_var, 1)[0]
        relaxed_var.remove(x)
        C.append(x >= 1)
        best1, solution1 = branch_and_bound(A, obj_func, C, relaxed_var, best, solution)
        del C[-1]
        C.append(x <= 0)
        best2, solution2 = branch_and_bound(A, obj_func, C, relaxed_var, best, solution)
        del C[-1]
        relaxed_var.add(x)
        if best1 > best2:
            return best1, solution1
        else:
            return best2, solution2     

    
def solve(n, k, M):
    adjacency_lists = matrix_to_adjacency_list(M)
    min_paths = minimal_infeasible_path(adjacency_lists, k)

    A = get_variables(n, 'Continuous')
    obj_func = get_obj_func(A)
    C = get_constraints(A, k, M, min_paths)

    relaxed_var = set()
    for a in A:
        for x in a:
            relaxed_var.add(x)

    best, solution = branch_and_bound(A, obj_func, C, relaxed_var, 0, [])

    return best, solution


def solve_file(file):
    n, k, M = loadtxt(file)
    return solve(n, k, M)

from minimal_infeasible_paths import minimal_infeasible_path
from timeit import Timer
from utils import loadtxt, matrix_to_adjacency_list


def time_for_minimal_infeasible_paths(number=1000):
    dataset_files = ["dataset/test1.txt", "dataset/test2.txt", "dataset/test3.txt"]
    for file in dataset_files:
        _, k, M = loadtxt(file)
        adjacency_lists = matrix_to_adjacency_list(M)
        t = Timer(lambda: minimal_infeasible_path(adjacency_lists, k))
        print(
            "{} -> mean time is {} milliseconds over {} iterations".format(
                file, t.timeit(number=number) / number * 1000, number
            )
        )


time_for_minimal_infeasible_paths()

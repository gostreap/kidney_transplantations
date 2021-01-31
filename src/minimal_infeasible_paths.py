from utils import loadtxt, matrix_to_adjacency_list


def minimal_infeasible_path(adjacency_lists, k):
    paths = []
    for v in range(len(adjacency_lists)):
        paths.extend(minimal_infeasible_path_from_vertex(adjacency_lists, v, k, set()))
    return paths


def minimal_infeasible_path_from_vertex(adjacency_lists, v, k, inpath):
    # print(k)
    if k == 0:
        # print("return")
        return [[v]]
    paths = []
    inpath.add(v)
    for neighbour in adjacency_lists[v]:
        # print("all", v, neighbour, inpath)
        if neighbour not in inpath:
            # print("else", v, neighbour)

            for path in minimal_infeasible_path_from_vertex(adjacency_lists, neighbour, k-1, inpath):
                paths.append([v] + path)

    inpath.remove(v)
    return paths


# _, k, M = loadtxt("dataset/test1.txt")
# adjacency_lists = matrix_to_adjacency_list(M)
# print(str(len(adjacency_lists)), "-", str(sum([len(adjacency_list) for adjacency_list in adjacency_lists])))
# print("test 1:", len(minimal_infeasible_path(adjacency_lists, k)))
# _, k, M = loadtxt("dataset/test2.txt")
# adjacency_lists = matrix_to_adjacency_list(M)
# print(len(adjacency_lists), "-", sum([len(adjacency_list) for adjacency_list in adjacency_lists]))
# print("test 2:", len(minimal_infeasible_path(adjacency_lists, k)))
# _, k, M = loadtxt("dataset/test3.txt")
# adjacency_lists = matrix_to_adjacency_list(M)
# print(len(adjacency_lists), "-", sum([len(adjacency_list) for adjacency_list in adjacency_lists]))
# print("test 3:", len(minimal_infeasible_path(adjacency_lists, k)))
# minimal_infeasible_path_from_vertex(adjacency_lists, 1, k, set())
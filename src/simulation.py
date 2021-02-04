from random import random, shuffle
from direct_donation import direct_donation
from greedy_matching import greedy_matching
from cycles_and_chains_matching import cycles_and_chains_matching


def get_random_blood_type():
    r = random()
    if r <= 0.46:
        return "O"
    if r <= 0.85:
        return "A"
    if r <= 0.96:
        return "B"
    else:
        return "AB"


def is_compatible(patient, donor):
    if donor == "O":
        return True
    elif donor == "A" and (patient == "A" or patient == "AB"):
        return True
    elif donor == "B" and (patient == "B" or patient == "AB"):
        return True
    elif donor == "AB" and patient == "AB":
        return True


def generate_data(n, c):
    patients = [get_random_blood_type() for _ in range(n)]
    donors = [get_random_blood_type() for _ in range(n)]
    cadavers = [get_random_blood_type() for _ in range(c)]

    K = []
    for i in range(n):
        K.append(set())
        for j in range(n):
            if is_compatible(patients[i], donors[j]):
                K[i].add(j)

    P = []
    for i in range(n):
        P.append([-1 for _ in range(n + 1)])
        order = list(K[i])
        shuffle(order)
        max = len(order)
        if i not in K[i]:
            max += 1
            if random() <= 0.5:
                P[i][i], P[i][n] = 1, 0
            else:
                P[i][i], P[i][n] = 0, 1
        else:
            P[i][n] = 0

        for j, e in enumerate(order):
            if e != i:
                P[i][e] = max - j

    return patients, donors, cadavers, K, P


def write_data(file, patients, donors, cadavers, K, P):
    f = open(file, "w")
    f.write("{}\n".format(len(patients)))
    f.write("{}\n".format(len(cadavers)))

    for i, patient in enumerate(patients):
        if i == 0:
            f.write("{}".format(patient))
        else:
            f.write(" {}".format(patient))
    f.write("\n")
    for i, donor in enumerate(donors):
        if i == 0:
            f.write("{}".format(donor))
        else:
            f.write(" {}".format(donor))
    f.write("\n")
    for i, cadaver in enumerate(cadavers):
        if i == 0:
            f.write("{}".format(cadaver))
        else:
            f.write(" {}".format(cadaver))
    f.write("\n")

    for k in K:
        for i, e in enumerate(k):
            if i == 0:
                f.write("{}".format(e))
            else:
                f.write(" {}".format(e))
        f.write("\n")

    for p in P:
        for i, e in enumerate(p):
            if i == 0:
                f.write("{}".format(e))
            else:
                f.write(" {}".format(e))
        f.write("\n")


def read_data(file):
    f = open(file, "r")
    lines = f.readlines()

    n = int(lines[0])
    c = int(lines[1])
    patients = lines[2].split()
    donors = lines[3].split()
    cadavers = lines[4].split()

    K = []
    for i in range(n):
        K.append(set(map(int, lines[i + 5].split())))

    P = []
    for i in range(n):
        P.append(list(map(int, lines[i + n + 5].split())))

    return n, c, patients, donors, cadavers, K, P


def gen_question_13():
    for i in range(1, 101):
        patients, donors, cadavers, K, P = generate_data(30, 3)
        write_data(
            "dataset/question_13_number_{}".format(i), patients, donors, cadavers, K, P
        )


def get_stat_of_matching(M):
    total = 0
    for (u, v) in M:
        if u == v:
            total += 1
        else:
            total += 2
    return total


def get_list_of_assigned_from_matching(M):
    assigned = set()
    for (u, v) in M:
        assigned.add(u)
        assigned.add(v)
    return list(assigned)


def get_not_assigned_from_assigned(assigned):
    total = set(range(30))
    return list(total - set(assigned))


def greedy_preprocess(n, K, P, U):
    M, _ = direct_donation(n, K)
    assigned = get_list_of_assigned_from_matching(M)
    is_matched = [False for u in U]
    for a in assigned:
        is_matched[a] = True
        assigned = get_list_of_assigned_from_matching(M)
    M = greedy_matching(n, K, P, U, is_matched=is_matched)
    assigned = assigned + get_list_of_assigned_from_matching(M)
    return assigned


def run_all():
    dd = []
    gm = []
    gmp = []
    cc = []
    for i in range(1, 101):
        print("run", i)
        n, c, patients, donors, cadavers, K, P = read_data(
            "dataset/question_13_number_{}".format(i)
        )
        U= list(range(30))

        M, w = direct_donation(n, K)
        assigned = get_list_of_assigned_from_matching(M)
        not_assigned = get_not_assigned_from_assigned(assigned)
        not_assigned_mean_rank = sum(not_assigned) / len(not_assigned) if len(not_assigned) != 0 else 30

        dd.append((len(assigned), not_assigned_mean_rank))

        M = greedy_matching(n, K, P, U)
        assigned = get_list_of_assigned_from_matching(M)
        not_assigned = get_not_assigned_from_assigned(assigned)
        not_assigned_mean_rank = sum(not_assigned) / len(not_assigned) if len(not_assigned) != 0 else 30

        gm.append((len(assigned), not_assigned_mean_rank))

        assigned = greedy_preprocess(n, K, P, U)
        not_assigned = get_not_assigned_from_assigned(assigned)
        not_assigned_mean_rank = sum(not_assigned) / len(not_assigned) if len(not_assigned) != 0 else 30

        gmp.append((len(assigned), not_assigned_mean_rank))

        M = cycles_and_chains_matching(n, K, P, U)
        assigned = get_list_of_assigned_from_matching(M)
        not_assigned = get_not_assigned_from_assigned(assigned)
        not_assigned_mean_rank = sum(not_assigned) / len(not_assigned) if len(not_assigned) != 0 else 30

        cc.append((len(assigned), not_assigned_mean_rank))

    dd_assigned_mean, dd_not_assigned_mean_rank = 0, 0
    gm_assigned_mean, gm_not_assigned_mean_rank = 0, 0
    gmp_assigned_mean, gmp_not_assigned_mean_rank = 0, 0
    cc_assigned_mean, cc_not_assigned_mean_rank = 0, 0

    for i in range(100):
        dd_assigned_mean += dd[i][0]
        dd_not_assigned_mean_rank += dd[i][1]
        gm_assigned_mean += gm[i][0]
        gm_not_assigned_mean_rank += gm[i][1]
        gmp_assigned_mean += gmp[i][0]
        gmp_not_assigned_mean_rank += gmp[i][1]
        cc_assigned_mean += cc[i][0]
        cc_not_assigned_mean_rank += cc[i][1]

    print(dd_assigned_mean / 100 / 30, dd_not_assigned_mean_rank / 100)
    print(gm_assigned_mean / 100 / 30, gm_not_assigned_mean_rank / 100)
    print(gmp_assigned_mean / 100 / 30, gmp_not_assigned_mean_rank / 100)
    print(cc_assigned_mean / 100 / 30, cc_not_assigned_mean_rank / 100)


# gen_question_13()
# run_all()

# for i in range(1, 10):
#     n, c, patients, donors, cadavers, K, P = read_data(
#                 "dataset/question_13_number_{}".format(i)
#             )
#     U = list(range(n))
#     cycles_and_chains_matching(n, K, P, U)

n, c, patients, donors, cadavers, K, P = read_data(
                "dataset/question_13_number_{}".format(3)
            )
U = list(range(n))
cycles_and_chains_matching(n, K, P, U)
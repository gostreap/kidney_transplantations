from random import random, shuffle


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
        write_data("dataset/question_13_number_{}".format(i), patients, donors, cadavers, K, P)


gen_question_13()

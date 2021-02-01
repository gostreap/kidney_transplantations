from utils import generate_data


def direct_donation(n, K):
    """
    Return a list of couple donor-patient c and a waiting list w
    """
    c, w = [], []
    for i in range(n):
        if i in K[i]:
            c.append((i, i))
        else:
            w.append(i)
    return c, w


def run_random(n):
    n, K, _, _ = generate_data(n)
    for i in range(n):
        print(i, "->", K[i])
    return direct_donation(n, K)


c, w = run_random(5)
print("c ->", c)
print("w ->", w)

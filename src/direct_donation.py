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

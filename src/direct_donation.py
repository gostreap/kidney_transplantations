from utils import loadtxt


def direct_donation(path):
    n, K, M = loadtxt(path)
    print(n)
    print(K)
    print(M)


direct_donation("dataset/test1.txt")

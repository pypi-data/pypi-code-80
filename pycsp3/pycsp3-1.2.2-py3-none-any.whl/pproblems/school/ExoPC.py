from pycsp3 import *

x = VarArray(size=4, dom=range(4))

satisfy(
    x[i] != x[j] for i, j in combinations(range(4), 2)
)

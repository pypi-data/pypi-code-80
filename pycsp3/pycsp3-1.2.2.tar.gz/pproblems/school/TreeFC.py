from pycsp3 import *

x1 = Var(0, 1, 2, 3)
x2 = Var(0, 1, 2, 3)
x3 = Var(0, 1, 2, 3)
x4 = Var(2, 3)
x5 = Var(2, 3)

satisfy(
    x1 != x2,
    x1 != x3,
    x2 != x3,
    x2 != x4,
    x2 != x5,
    x3 != x4,
    x3 != x5,
    x4 != x5
)

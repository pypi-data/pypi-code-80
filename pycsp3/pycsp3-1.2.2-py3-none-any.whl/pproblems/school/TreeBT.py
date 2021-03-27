from pycsp3 import *

x1 = Var(1, 2, 3)
x2 = Var(1, 2, 3)
x3 = Var(1, 2, 3)
x4 = Var(1, 2, 3)

satisfy(
    x1 != x2,
    x1 >= x2 + x3,
    2 * x1 <= x2 * x4
)

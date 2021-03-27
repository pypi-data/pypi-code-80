from pycsp3 import *

x = Var(1, 2, 3)
y = Var(1, 2, 3)
z = Var(1, 2, 3)

satisfy(
    x >= y,
    y >= z,
    x != z
)

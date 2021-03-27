from pycsp3 import *

w = Var(1, 2, 3)
x = Var(1, 2, 3)
y = Var(1, 2, 3)
z = Var(1, 2, 3)

satisfy(
    w >= x,
    x >= y,
    y >= z,
    w != z,
    (x, z) in {(1, 3), (2, 2), (3, 1)}
)

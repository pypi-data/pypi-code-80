from pycsp3 import *

x = Var(0, 1, 2)
y = Var(0, 1, 2)
z = Var(0, 1, 2)

satisfy(
    x > y,
    y != z
)

maximize(
    x + y + z
)

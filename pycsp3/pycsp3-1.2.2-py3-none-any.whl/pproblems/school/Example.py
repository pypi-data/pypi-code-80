from pycsp3 import *

w = Var(range(1,4))
x = Var(range(1,4))
y = Var(range(1,5))
z = Var(range(1,5))

satisfy(
    x == y,
    x <= y +1,
    y >= w + z,
    (x, z) in {(1, 2), (2,1), (2, 4), (3, 3)}
)

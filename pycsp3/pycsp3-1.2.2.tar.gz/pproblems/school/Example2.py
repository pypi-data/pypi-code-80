from pycsp3 import *

w = Var(1,2,3)
x = Var(1,2,3)
y = Var(1,2,3,4)
z = Var(1,2,3,4,)

satisfy(
    w == x,
    x <= y +1,
    y > z,
    (x, z) in {(1, 2), (2,1), (2, 4), (3, 3)}
)
import numpy as np

def foo(x,y,z):
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    return (x+y) * z

def print_foo(x,y,z):
    return print(foo(x,y,z))

def foo2(number, string):
    print(number + number)
    print(string)
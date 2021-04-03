import pyo
import numpy as np

print(
    """
    WELLUM to PEEPO

    """
)

width = 20

for i in range(25):
    w = np.random.randint(4, width)
    dish = np.random.randint(0, max([0, width - w]))

    print(' '*w + 'pee' + ' '*dish + 'po')

import random
import os
import sys


def RTrue(perc):
    if perc > 100:
        raise ValueError("The percentage must not be greater than 100%")
    num1 = 1
    num100 = 100
    RN = random.randint(num1,num100)
    if isinstance(perc, float):
        num0 = 0
        RN = random.uniform(num0, num100)
    if RN <= perc:
        return True
    else:
        return False

def RFalse(perc):
   if RTrue(perc):
       return False
   else:
       return True



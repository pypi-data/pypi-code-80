def wgt_in_pounds(x):
    p=x/2.54
    return p


Kgs=wgt_in_pounds(int(input("Enter Weight in Pounds:")))
print(f"Weight in Kgs:{Kgs}")
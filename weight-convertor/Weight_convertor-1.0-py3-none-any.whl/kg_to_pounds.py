def wgt_in_kg(x):
    p=x*2.54
    return p


pounds=wgt_in_kg(int(input("Enter Weight in Kgs:")))
print(f"Weight in Pounds:{pounds}")

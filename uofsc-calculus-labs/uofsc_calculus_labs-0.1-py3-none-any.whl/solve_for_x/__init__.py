def solve_for_x(sub,x):
    a = 0
    b = pi/2
    xTest = uniform(a, b)
    uTest = sub.rhs().substitute(x = xTest)
    
    ## If first test point was not in domain, then choose a different test point in a range which gets wider and wider
    if (imag(uTest) != 0):
        count = 0
        while(imag(uTest) != 0):
            a = 0 - 10^count
            b = 10 + 10^count
            xTest = randint(a, b)
            uTest = sub.rhs().substitute(x = xTest)
            count = count + 1
    
    ## Find the correct solution. Had to round for precision issues
    for i in solve(sub,x):
        if(imag(i.rhs().substitute(u=uTest)) == 0):
            xTest = round(xTest,6)
            test = round(i.rhs().substitute(u = uTest),6)
            if (xTest == test):
                return i
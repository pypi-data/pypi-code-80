def gen_from(gen):
    if gen[0]:
        for i in range(len(gen[1])):
            gen[1][i] = gen[1][i].replace('a','u')
            gen[1][i] = gen[1][i].replace('t','a')
            gen[1][i] = gen[1][i].replace('c','g')
            gen[1][i] = gen[1][i].replace('g','c')
    return gen
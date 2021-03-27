def read(path):
    try:
        gen = None
        with open(path, mode='r', encoding='utf8') as r:
            gen = r.readlines()
            return (True,gen)
    except:
        return (False,None)
    
def plot(sequence):
    if sequence[0]:
        for i in sequence[1]:
            # Remove \n in final
            print(i[:-1])
    else:
        print('the gene is corrupted')
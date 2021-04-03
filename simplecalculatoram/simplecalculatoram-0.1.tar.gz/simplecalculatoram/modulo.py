# https://www.youtube.com/watch?v=Qs91v2Tofys
def add(n, n2):
    if (n != int and n !=float or n2 != int and n2 !=float):
        raise ValueError("Hay que especificar valores")
    return n + n2

def goodbye():
    print("Hola, te estoy saludando desde la función saludar() " \
            "del módulo saludos")
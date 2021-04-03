def primo(n):
    if n > 1:

        if n==2:
            print("2")
        else:
            x = 0
            for i in range(2, n+1):
                c = 0
                
                for j in range(2, i+1):
                    
                    if (i % j) == 0:
                        c = c+1
                
                if c == 1:
                    print (i, end=" ")
                    x = x+1
            
            print("\n")
            print ("Entre 2 y",n, "existen",x, "numeros primos")    

    else:
        print ("Debe insertar un numero entero mayor que 1")


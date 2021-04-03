# Haciendo uso de la librería rpy2, 
# implemente una función en R para calcular 
# los números primos entre 1 y n, donde n es 
# un parámetro de la función.
import rpy2.robjects as ro

codigo_r = """
CribaEratostenesR <- function(n)
{
   n <- as.integer(n)
   primes <- rep(TRUE, n)
   last.prime <- 2L
   if(n > 3){
        for(i in last.prime:floor(sqrt(n))){
            primes[seq.int(2L*last.prime, n, last.prime)] <- FALSE
            last.prime <- last.prime + min(which(primes[(last.prime+1):n]))
        }
   }
   print(which(primes))
}

EsPrimo_r <- function(n)
{
    primo = 1
    if(n >= 4){
       for(i in 2:floor(sqrt(n))){
          if(n %% i == 0){
             primo = 0
          }
        }
    }
    if(primo == 1){
       TRUE
    }else{
       FALSE
    }
}

NumPrimos_r <- function(n)
{
    primos<-vector()
    for(i in 1:n)
   {
      if(EsPrimo_r(i)){
          primos <- c(primos, i)
      }
   }

print(primos)
}

"""
ro.r(codigo_r)

#1.funcion criba de eratostenes
 #https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Algorithm_and_variants
 #dado el numero n -> eliminamos todos los multiples (de 2 a sqrt(n)) hasta llegar a n
 #NumerosPrimos1(n)

CribaEratostenes_py = ro.globalenv['CribaEratostenesR']

def NumerosPrimos1(n):
    if(n > 0):
        if(n != 1):
            CribaEratostenes_py(n)
        else:
            print(1)
    else:
        print("Error! introduce un número entero psitivo")
    


#2.funcion propia:
# funcion esPrimo(n) -> dado un numero n -> n%[2..sqrt(n)]
# si es 0 el numero NO es primo 
#NumerosPrimos2(n) de 1 a n NumPrimos_r -> esPrimo

NumPrimos_py = ro.globalenv['NumPrimos_r']

def NumerosPrimos2(n):
    if(n > 0):
        NumPrimos_py(n)
    else:
        print("Error! introduce un número entero psitivo")  

#test
#NumerosPrimos1(100)
#NumerosPrimos2(100)

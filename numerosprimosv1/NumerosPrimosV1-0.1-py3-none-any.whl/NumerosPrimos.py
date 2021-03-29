# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 18:51:56 2021

@author: Antonio
"""

def primo(nump):
    
 if nump < 2: 
   return False
 for p in range(2, nump): 
   if nump % p == 0: 
  return False
return True 


n= int(input("Introduce un número"))
valor= range(2,n)
contador= 1

for numero in valor:
  if primo(numero) == True:
    contador += 1
        print(numero)
    
print("Hay", contador,"numeros primos entre 1 y", n)
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 18:32:15 2021

@author: david
"""

def primo(num):
 if num < 2: 
   return False
 for i in range(2, num):
   if num % i == 0: 
    return False
 return True 


n = int (input("¿Qué números quieres saber si son primos?"))
valor= range (2,n)
contador = 1
for numero in valor:
  if primo(numero) == True:
    contador +=1
    print(numero)
    
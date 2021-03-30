# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 17:25:24 2021

@author: jinie
"""
from rpy2.robjects import r 
def numerosPrimos(b):
        r.assign('v', b)
        r('''  
        for (i in 1:v){
                a <- 1
                if (i > 2){
                     for (n in 2:(i - 1)){
                             c <- (i%%n)
                             if (c == 0){
                                     a <-0
                                }
                        }   
                }
                if (a == 1){
                        print(i) 
                }  
        }
        ''')

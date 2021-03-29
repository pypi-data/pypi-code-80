import rpy2.robjects as r

codigo_r = '''
listaprimo <- function(n){
  if (n<=0)
  {
    print("Error, el valor debe de ser positivo únicamente")}
    
  else if (n==1)
  {
      print("El numero debe de ser mayor a 1") }
  else if (n>1)
  {  
    for (i in 2:n)
    {
      es_primo <- 1
      j <-2
      while(j <= sqrt(i))
      {
        if (i%%j==0)
        {
          es_primo <- 0 
        }
        j <- j+1
      }
      if(es_primo==1)
      {
        print(i)
      
      }
    }
  }
}
'''
r.r(codigo_r)

primo = r.globalenv['listaprimo']
	
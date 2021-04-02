import rpy2.robjects as ro

def prime_numbers (n):
    """
    Create a list of prime number from 1 to n
    input:
        n = number until have to find prime numbers
    """

    function = """
        prime_function <- function(n){
          prime_list <- c(2)
          if (n > 2){
            for (number in 2:n){
              prime_flag <- TRUE
              for (prime in prime_list){
                if ((number %% prime) == 0){
                  prime_flag <- FALSE
                  break
                }
              }
              if (prime_flag){
                prime_list <- c(prime_list, number)
              }
            }
          }
          cat('Los numero primo entre 1 y ',n,' son: ') 
          cat(prime_list)
        }
    """

    ro.r(function)
    prime_py = ro.globalenv['prime_function']
    prime_py(n)
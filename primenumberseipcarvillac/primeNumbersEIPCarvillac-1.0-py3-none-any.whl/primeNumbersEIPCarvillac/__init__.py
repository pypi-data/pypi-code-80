import rpy2.robjects as ro

r_code = """


primes <- function(n){
    for (i in 1:n){
        if(i==2){
                print(i)
        } else {
            if(all(i %% (2:sqrt(i)) != 0)){
                print(i)
            }
        }
    }
}
"""

ro.r(r_code)

primes_py = ro.globalenv['primes']


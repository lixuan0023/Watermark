import gmpy2
from gmpy2 import mpz

add = mpz('1')+mpz('2')
print(add)
sub = mpz('2')-mpz('1')
print(sub)
mul = mpz('2')*mpz('3')
print(mul)
div = mpz('2')/mpz('3')
print(div)
power = mpz('2')**mpz('3')
print(power)
mod = mpz('12')%mpz('3')
print(mod)

state = gmpy2.random_state(6666667)
random = gmpy2.mpz_random(state,mpz('999999999999999'))
print(random,type(random))

prime = gmpy2.next_prime(10000009999)
print(prime)



import gmpy2
from gmpy2 import mpz

# add = mpz('1')+mpz('2')
# print(add)
# sub = mpz('2')-mpz('1')
# print(sub)
# mul = mpz('2')*mpz('3')
# print(mul)
# div = mpz('2')/mpz('3')
# print(div)
# power = mpz('2')**mpz('3')
# print(power)
# mod = mpz('12')%mpz('3')
# print(mod)

state = gmpy2.random_state(6666667)
random = gmpy2.mpz_random(state,mpz('999999999999999'))
print(random,type(random))

random = gmpy2.mpz_rrandomb(state,2048)
random = gmpy2.mpz_urandomb(state,2048)

num = random.num_digits(2)
print(num,type(num))

prime = gmpy2.next_prime(10000009999)
print(prime)

num_mpz = mpz(4444444)
num = num_mpz.num_digits(2)
print(num,type(num))

a = gmpy2.mpq(2)
print(type(a.numerator))

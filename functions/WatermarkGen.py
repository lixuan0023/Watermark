import numpy as np

mu,sigma = 0,1
s = np.random.normal(mu,sigma, 100)

w = s[0]
x = 63334.25
alpha = 0.01
xn = x*(1+alpha*w)

print('w ',w)
print('xn ',xn)

t = xn-x
wn = t/(alpha*x)
print('wn ',np.float32(wn))

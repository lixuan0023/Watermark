import numpy as np
# Create a copy of the array with 
# the value of the element in k-th position.


a = np.array([[7,8,9],[4,5,6],[1,2,3]])
p = np.reshape(a,-1)
print(p)


idx = np.argsort(p)[-3:]
idx_2d = np.unravel_index(idx[0],a.shape)

print(idx)
print(p[idx])
print(idx_2d)



import numpy as np
# Create a copy of the array with
# the value of the element in k-th position.


a = np.array([[7,8,9],[4,5,6],[1,2,3]])
p = np.reshape(a,-1)
print(p)


idx = np.argsort(p)[-3:]

# for x in range(idx.size):
#     print(np.unravel_index(idx[x],a.shape))

ls = [np.unravel_index(idx[x],a.shape) for x in range(idx.size) ]
print(ls)
# print(idx)
# print(p[idx])
# print(a[idx_2d])



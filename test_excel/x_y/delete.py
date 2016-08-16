import numpy as np


data_x = np.loadtxt('dummy.csv', delimiter = ',')


print data_x

data_x = np.delete(data_x, np.s_[13:14:], 1)

print data_x

#test = np.([1,2,3], [1,2,3], [1,2,3])
#print test
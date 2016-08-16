import numpy as np 


data_x = np.array([[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]])

data_x = np.delete(data_x, np.s_[1::2],1)
#data_x = np.delete(data_x, np.s_[13:14:], 1)


print data_x



print data_x


"""
deleted length and last 5 features -> probability doropped to 66max and predicitions were pretty much 50:50
kept length -> probability jumped way up to 78 during training but would still predict many way wrong or 50:50
deleted only last two google words features up to 80 yeay!
"""
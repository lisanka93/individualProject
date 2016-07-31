import numpy as np


def load_data():


	data_y = np.loadtxt('y.csv', delimiter = ',')

	#print data_y

	#print data_y.shape
	data_x = np.loadtxt('x.csv', delimiter = ',')

	#print data_x.shape

	#print data_x
		
	out = []

	for i in range(data_x.shape[0]):
 		fart = list((data_x[i].tolist(), data_y[i].tolist())) # don't mind this variable name
		out.append(fart)
	

	print out



X = load_data()
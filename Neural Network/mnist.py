'''
A Multilayer Perceptron implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

# Import MINST data
import numpy as np

import tensorflow as tf

# Parameters
learning_rate = 0.001
training_epochs = 100
batch_size = 100
display_step = 1

# Network Parameters
n_hidden_1 = 10 # 1st layer number of features
n_hidden_2 = 5 # 2nd layer number of features
n_input = 26 # MNIST data input (img shape: 28*28)
n_classes = 2# MNIST total classes (0-9 digits)

# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])


# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return tf.nn.softmax(out_layer)

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1], mean = 0.01)),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2],  mean = 0.01)),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes],  mean = 0.01))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1],  mean = 0.01)),
    'b2': tf.Variable(tf.random_normal([n_hidden_2],  mean = 0.01)),
    'out': tf.Variable(tf.random_normal([n_classes],  mean = 0.01))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost = -tf.reduce_sum(y * tf.log(tf.clip_by_value(pred, 1e-10, 1.0)))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.initialize_all_variables()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.

        data_y = np.loadtxt('y.csv', delimiter = ',')

        data_x = np.loadtxt('x.csv', delimiter = ',')
        data_x = np.delete(data_x, np.s_[:1],1)
        data_x = np.delete(data_x, np.s_[13:14:], 1)

        #print data_x.shape
        #print data_y.shape


        total_batch = int(data_x.shape[0]/batch_size)
        print total_batch
        # Loop over all batches
        for i in range(total_batch):
            left = batch_size*i
            right = batch_size*(i+1)
            # Run optimization op (backprop) and cost op (to get loss value)

            #print data_x[left:right,:]
            #print data_y[left:right,:]
            _, c = sess.run([optimizer, cost], feed_dict={x: data_x[left:right,:],
                                                          y: data_y[left:right,:]})





            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        if epoch % display_step == 0:
            print "Epoch:", '%04d' % (epoch+1), "cost=", \
                "{:.9f}".format(avg_cost)
    print "Optimization Finished!"

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print "Accuracy:", accuracy.eval({x: data_x, y: data_y})



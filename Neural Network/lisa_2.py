
import numpy as np
import tensorflow as tf

LEARNING_RATE = 0.001
DROPOUT_RATE = 0.8
BATCH_SIZE = 100
NUMBER_OF_EPOCHS = 10

data_x = np.loadtxt('x.csv',delimiter=',')
data_y = np.loadtxt('y.csv',delimiter=',')

# Make sure all the values are between 0 and 1
for i in xrange(data_x.shape[1]):
    maxval = data_x[:,i].max()
    if maxval != 0.0:
        data_x[:,i] = data_x[:,i]/maxval

# Use the cpu instead of gpu
with tf.device('/cpu:0'):

    features = data_x.shape[1]
    # INPUT
    x = tf.placeholder(tf.float32, [None, features],name='input')
    # HIDEEN LAYER
    W1 = tf.Variable(tf.zeros([features, 14]))
    b1 = tf.Variable(tf.zeros([14]))
    hidden_layer = tf.nn.sigmoid(tf.matmul(x, W1) + b1)

    # DROPOUT
    keep_prob = tf.placeholder(tf.float32)
    hidden_layer_drop = tf.nn.dropout(hidden_layer, keep_prob)

    # FINAL LAYER
    W2 = tf.Variable(tf.zeros([14, 2]))
    b2 = tf.Variable(tf.zeros([2]))
    y = tf.nn.softmax(tf.matmul(hidden_layer_drop, W2) + b2) # Softmax on the ouput ensures the output adds up to 1 (so it is a probability)
    y_ = tf.placeholder(tf.float32, [None, 2],name='output')

    # COST
    loss = -tf.reduce_sum(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))/float(features)

    # ACCURACY
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1)) # Answer is correct if both y and y_ share the same argmax
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # TRAIN
    train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss) # use the adam optimizer because it's made out of magic

    # TENSORFLOW STUFF
    init = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init)

    for e in range(NUMBER_OF_EPOCHS):
        print 'epoch', e
        for i in range(data_x.shape[0]/BATCH_SIZE):
          left = BATCH_SIZE*i
          right = BATCH_SIZE*(i+1)
          _, c = sess.run([train_step,loss], feed_dict={x: data_x[left:right], y_: data_y[left:right], keep_prob : DROPOUT_RATE})
        print 'cost = ', sess.run(loss, feed_dict={x: data_x, y_: data_y, keep_prob : 1.0}),
        print 'accu = ', sess.run(accuracy, feed_dict={x: data_x, y_: data_y, keep_prob : 1.0})

    # Finally run all the data through the network to get the predictions
    y_pred = sess.run(y, feed_dict={x: data_x, keep_prob : 1.0})

    def nicestr(x):
        s = '['
        for y in x:
            s += str(round(y,2)) + ' '
        s += ']'
        return s

    # Print some examples to see what is going on
    for i in xrange(0,data_x.shape[0],500):
        print i, nicestr(data_x[i]), nicestr(data_y[i]), nicestr(y_pred[i])
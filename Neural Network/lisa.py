import numpy as np
import tensorflow as tf

LEARNING_RATE = 0.01
DROPOUT_RATE = 0.8
BATCH_SIZE = 1
NUMBER_OF_EPOCHS = 100


#best result if hidden layer neurons more or less half of input neurons
#havent changes putput neurons yet because need to rearrange data
#optimum dropour rate is 0.8
#precentage increases if batchsize is reduced however thats might due to overfitting? 
#batch size 100 = 80%, batch size = 1 = 84%


data_x = np.loadtxt('x.csv',delimiter=',')
data_y = np.loadtxt('y.csv',delimiter=',')


print data_x.shape


# Make sure all the values are between 0 and 1
for i in xrange(data_x.shape[1]):
    maxval = data_x[:,i].max()
    if maxval != 0.0:
        data_x[:,i] = data_x[:,i]/maxval
        print data_x[:,i]


# Use the cpu instead of gpu
with tf.device('/cpu:0'):

    features = data_x.shape[1]
    print features
    # INPUT
    x = tf.placeholder(tf.float32, [None, features],name='input')
    # HIDEEN LAYER
    W1 = tf.Variable(tf.zeros([features, 26]))  #13
    b1 = tf.Variable(tf.zeros([26]))#13
    hidden_layer = tf.nn.sigmoid(tf.matmul(x, W1) + b1)

    # DROPOUT
    keep_prob = tf.placeholder(tf.float32)
    hidden_layer_drop = tf.nn.dropout(hidden_layer, keep_prob)

    # FINAL LAYER
    W2 = tf.Variable(tf.zeros([26, 2]))  #13
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



    data_xtest = np.loadtxt('x_test.csv',delimiter=',')
    data_ytest = np.loadtxt('y_test.csv',delimiter=',')


    

    for i in xrange(data_xtest.shape[1]):
        maxval = data_xtest[:,i].max()
        if maxval != 0.0:
            data_xtest[:,i] = data_xtest[:,i]/maxval


    y_pred = sess.run(y, feed_dict={x: data_xtest, keep_prob : 1.0})

    def nicestr(x):
        s = '['
        for y in x:
            s += str(round(y,2)) + ' '
        s += ']'
        return s

    # Print some examples to see what is going on
    for i in xrange(0,data_xtest.shape[0],1):
        print i, nicestr(data_xtest[i]), nicestr(data_y[i]), nicestr(y_pred[i])

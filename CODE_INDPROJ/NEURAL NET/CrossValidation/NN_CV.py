import numpy as np
import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
import time


#NETWORK PARAMETERS
LEARNING_RATE = 0.01
DROPOUT_RATE = 1
BATCH_SIZE = 100
NUMBER_OF_EPOCHS = 10
hidden_neurons = 2

#TRAINING DATA + TEST DATA
data_x = np.loadtxt('1_x_train.csv',delimiter=',') 
data_y = np.loadtxt('1_y_train.csv',delimiter=',') 
data_xtest = np.loadtxt('1_x_test.csv',delimiter=',') 
data_ytest = np.loadtxt('1_y_test.csv',delimiter=',')

#choice of features to exclude
#data_x = np.delete(data_x, np.s_[19,55,10,46,15,51,20,56,32,68,33,69,1,37, 6,42, 13,49, 16,52,17,53,18,54, 23,59, 0,36, 4,40, 5,41,7,43,9,45,11,47,12,48,14,50,25,61,27,63,29,65,30,66,31,67,34,70,35,71,8,44,22,58,26,62,28,64,3,39,21,57,24,60],1)
#data_xtest = np.delete(data_xtest, np.s_[19,55,10,46,15,51,20,56,32,68,33,69,1,37, 6,42, 13,49, 16,52,17,53,18,54, 23,59, 0,36, 4,40, 5,41,7,43,9,45,11,47,12,48,14,50,25,61,27,63,29,65,30,66,31,67,34,70,35,71,8,44,22,58,62,26,3,28,64,39,21,57,24,60],1)

#I accidentaly counted advers twice in the vector, so I am deleting one value
data_x = np.delete(data_x, np.s_[19,55],1)
data_xtest = np.delete(data_xtest, np.s_[19,55],1)

# Make sure all the values are between 0 and 1
for i in xrange(data_x.shape[1]):
    maxval = data_x[:,i].max()
    if maxval != 0.0:
        data_x[:,i] = data_x[:,i]/maxval
        #print data_x[:,i]


# Use the cpu instead of gpu
with tf.device('/cpu:0'):
    start = time.time()

    samples = data_x.shape[0]
    features = data_x.shape[1]

    #print "samples", samples
    print "features", features
   

    # INPUT
    x = tf.placeholder(tf.float32, [None, features],name='input')
   
    # HIDEEN LAYER
    W1 = tf.Variable(tf.random_normal([features, hidden_neurons], mean = 0.0, stddev = 1.0, seed = 0))  #13
    b1 = tf.Variable(tf.random_normal([hidden_neurons], mean = 0.0, stddev = 1.0, seed = 0))#13
    hidden_layer = tf.nn.sigmoid(tf.matmul(x, W1) + b1)

    # DROPOUT
    keep_prob = tf.placeholder(tf.float32)
    hidden_layer_drop = tf.nn.dropout(hidden_layer, keep_prob)

    # FINAL LAYER
    W2 = tf.Variable(tf.random_normal([hidden_neurons, 2], mean = 0.0, stddev = 1.0, seed = 0))  #13
    b2 = tf.Variable(tf.random_normal([2], mean = 0.0, stddev = 1.0, seed = 0))
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
    #tf.set_random_seed(1)

    for e in range(NUMBER_OF_EPOCHS):
        #print 'epoch', e
        for i in range(data_x.shape[0]/BATCH_SIZE):
          left = BATCH_SIZE*i
          right = BATCH_SIZE*(i+1)
          _, c = sess.run([train_step,loss], feed_dict={x: data_x[left:right], y_: data_y[left:right], keep_prob : DROPOUT_RATE})
          #print "data", x  

        #print 'cost = ', sess.run(loss, feed_dict={x: data_x, y_: data_y, keep_prob : 1.0}),
        #print 'accu = ', sess.run(accuracy, feed_dict={x: data_x, y_: data_y, keep_prob : 1.0})

    # Finally run all the data through the network to get the predictions

    samples2 = data_xtest.shape[0]
    

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

    counter_wrong = 0
    counter_right = 0
    cant_decide = 0

    wrong_1 = 0
    wrong_2 = 0
    wrong_3 = 0
    fiftyfifty = 0
    print "wrong predictions:"
  
    # Print some examples to see what is going on
    for i in xrange(0,data_xtest.shape[0],1):
        #print i, nicestr(data_xtest[i]), nicestr(data_ytest[i]), nicestr(y_pred[i])
        #print nicestr(y_pred[i])

        """
        if round(y_pred[i][0],1)  > 0.4 and round(y_pred[i][0],1) < 0.6:
            #print y_pred[i][0]
            cant_decide +=1
            #print i+1, nicestr(data_xtest[i]), nicestr(data_ytest[i]), nicestr(y_pred[i])
        elif data_ytest[i][0] == round(y_pred[i][0]) and (round(y_pred[i][0],1) >= 0.6 or round(y_pred[i][0],1) <= 0.4) :

            counter_right +=1
        else:
            counter_wrong +=1
        """ 

        if data_ytest[i][0] == round(y_pred[i][0]):
            counter_right +=1
        else:
            counter_wrong +=1
            #print i
            print i+1, nicestr(y_pred[i])

            if (y_pred[i][0] >= 0.5 and y_pred[i][0] < 0.6) or (y_pred[i][1] >= 0.5 and y_pred[i][1] < 0.6) :
                wrong_1 +=1
                #print i+1, nicestr(data_xtest[i]), nicestr(data_ytest[i]), nicestr(y_pred[i])

            elif (y_pred[i][0] >= 0.6 and y_pred[i][0] < 0.78) or (y_pred[i][1] >= 0.6 and y_pred[i][1] < 0.78):
                wrong_2 +=1
                #print i+1, nicestr(data_xtest[i]), nicestr(data_ytest[i]), nicestr(y_pred[i])

            elif (y_pred[i][0] >= 0.78 and y_pred[i][0] <= 1) or (y_pred[i][1] >= 0.78 and y_pred[i][1] <= 1) :
                #print i+1, nicestr(data_xtest[i]), nicestr(data_ytest[i]), nicestr(y_pred[i])

                wrong_3 +=1
            else:
                fiftyfifty +=1
            


        
    correct_answers = (float(counter_right) / samples2)
    print "correct answers", correct_answers
    #cant_decide_answers = (float(cant_decide) / samples2)
    #print "cant decide", cant_decide_answers
    
    fiftyfifty1 = (float(fiftyfifty) / counter_wrong)
    #print "fiftyfifty", fiftyfifty1

    """
    print "counter wrong", counter_wrong
    #print "wrng counters", wrong_1, wrong_2, wrong_3

    wrong1 = (float(wrong_1) / counter_wrong)
    print "wrong1", wrong1

    wrong2 = (float(wrong_2) / counter_wrong)
    print "wrong2", wrong2

    wrong3 = (float(wrong_3) / counter_wrong)
    print "wrong3", wrong3
    #print "cant decide", cant_decide_answers

    """
    end = time.time()
    elapsed = end - start
    print "elapsed time", elapsed


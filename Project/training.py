import numpy as np
import random
import json
import tensorflow as tf
import matplotlib.pyplot as plt
import Q_learning_rough as api
import AgarBots as api2
import time

def setup():
    print("let's begin")
    api.createPlayer("kenneth-bot", "kenneth-bot")

def getRawStates():
    view = api2.getView("kenneth-bot")
    return api.getState(view, 8, 10, 10, "kenneth-bot")

def computeState(raw_states):
    state = np.arange(8)
    for index, item in enumerate(raw_states):
        state[index] = item[1] - item[0]
    return state.reshape((1,8))

tf.reset_default_graph()

#These lines establish the feed-forward part of the network used to choose actions
inputs1 = tf.placeholder(shape=[1,8],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([8,8],0,0.01))
Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,1)

#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[1,8],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)

init = tf.global_variables_initializer()

# Set learning parameters
y = .80
e = 0.5
num_episodes = 1000
#create lists to contain total rewards and steps per episode
jList = []
rList = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        #Reset environment and get first new observation
        setup()
        # s = env.reset()
        state = computeState(getRawStates())
        rAll = 0
        d = False
        j = 0
        #The Q-Network
        while j < 99:
            j+=1
            print(j)
            #Choose an action by greedily (with e chance of random action) from the Q-network
            a,allQ = sess.run([predict,Qout],feed_dict={inputs1:state})
            if np.random.rand(1) < e:
                a[0] = random.randint(0,8)
            #Get new state and reward from environment
            # s1,r,d,_ = env.step(a[0])
            api2.move("kenneth-bot", a[0])
            rawStates = getRawStates()
            newStates = computeState(rawStates)
            r = api.reward(rawStates)
            #Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout,feed_dict={inputs1:newStates})
            #Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0,a[0]] = r + y*maxQ1
            #Train our network using target and predicted Q values
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:state,nextQ:targetQ})
            rAll += r
            state = newStates
            if api2.isAlive("kenneth-bot") == False:
                #Reduce chance of random action as we train the model.
                e = 1./((i/50) + 10)
                break
        print('episode' + str(i) + 'ends')
        print(sess.run(W))
        jList.append(j)
        rList.append(rAll)
print("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")
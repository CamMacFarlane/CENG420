import numpy as np
import random
import csv
from nn import neural_net, LossHistory
import os.path
import time
import timeit
import AgarBots as ab
import Q_learning_rough as ql

REWARD_FOR_EATING = 15
NUM_INPUT = 16
GAMMA = 0.9  # Forgetting.
TUNING = False  # If False, just use arbitrary, pre-selected params.
STEP_DELAY = 0.1

botId = "WillyTestBot001"
botName = "Willy's test bot"

def get_max_sector(state):
    temp = state[0]
    max_sector = 0
    max_value = temp[0]
    k = 0

    for i in temp:
        if(i> max_value):
            max_sector = k
            max_value = i
        k= k+1
    return max_sector

def move_to(id,N,maxN):
    ql.move(id,N,maxN)

    time.sleep(STEP_DELAY)

    if(ab.isAlive(id)):
        state, massDelta = ql.getState(id)
        return ql.reward(state, massDelta),np.asarray(state)
    else:
        state = np.array([])
        ql.createPlayer(botName,botId)
        return -5000, state


def train_net(model, params):

    filename = "weight"

    observe = 300  # Number of frames to observe before training.
    epsilon = 1
    train_frames = 26000  # Number of frames to play.
    batchSize = params['batchSize']
    buffer = params['buffer']

    # Just stuff used below.
    max_travel_distance = 0
    travel_distance = 0
    t = 0
    data_collect = []
    replay = []  # stores tuples of (S, A, R, S').

    loss_log = []

    ql.createStaticBots(20)

    ql.createPlayer(botName,botId)

    # Create a new game instance.
    first_view = ab.getView(botId)

    # Get initial state by doing nothing and getting the state.
    first_action = random.randint(0,NUM_INPUT)
    _, state = move_to(botId,first_action,NUM_INPUT) # move_to will return the new view

    # Let's time it.
    start_time = timeit.default_timer()

    # Run the frames.
    while t < train_frames:

        print(t)
        t += 1
        travel_distance += 1

        # Choose an action.
        if random.random() < epsilon or t < observe:
            action = np.random.randint(0, NUM_INPUT)  # random
        else:
            # Get Q values for each action.
            qval = model.predict(state, batch_size=1)
            action = (np.argmax(qval))  # best

            action = get_max_sector(state)

        # Take action, observe new state and get our treat.

        reward, new_state = move_to(botId,action,NUM_INPUT)

        # Experience replay storage.
        replay.append((state, action, reward, new_state))


        # If we're done observing, start training.
        if t > observe:

            # If we've stored enough in our buffer, pop the oldest.
            if len(replay) > buffer:
                replay.pop(0)

            # Randomly sample our experience replay memory
            minibatch = random.sample(replay, batchSize)

            # Get training values.
            X_train, y_train = process_minibatch(minibatch, model)
            #print("X_train:")
            #print(X_train)
            #print('---------------------------')
            #print("y_train:")
            #print(y_train)
            #print('---------------------------')
            # Train the model on this batch.
            history = LossHistory()
            model.fit(
                X_train, y_train, batch_size=batchSize,
                epochs=1, verbose=0, callbacks=[history]
            )
            loss_log.append(history.losses)

        # Update the starting state with S'.
        state = new_state

        # Decrement epsilon over time.
        if epsilon > 0.1 and t > observe:
            epsilon -= (1/train_frames)

        # We died, so update stuff.
        if reward == -5000:
            # Log the car's distance at this T.
            data_collect.append([t, travel_distance])

            # Update max.
            if travel_distance > max_travel_distance:
                max_travel_distance = travel_distance

            # Time it.
            tot_time = timeit.default_timer() - start_time
            fps = travel_distance / tot_time

            # Output some stuff so we can watch.
            print("Max: %d at %d\tepsilon %f\t(%d)\t%f fps" %
                  (max_travel_distance, t, epsilon, travel_distance, fps))

            # Reset.
            travel_distance = 0
            start_time = timeit.default_timer()

        # Save the model every 25,000 frames.
        if t % 500 == 0:
            model.save_weights('saved-models/' + filename + '.h5', overwrite=True)
            print("Saving model %s - %d" % (filename, t))

    # Log results after we're done all frames.
    log_results(filename, data_collect, loss_log)


def log_results(filename, data_collect, loss_log):
    # Save the results to a file so we can graph it later.
    with open('results/sonar-frames/learn_data-' + filename + '.csv', 'w') as data_dump:
        wr = csv.writer(data_dump)
        wr.writerows(data_collect)

    with open('results/sonar-frames/loss_data-' + filename + '.csv', 'w') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)


def process_minibatch(minibatch, model):
    """This does the heavy lifting, aka, the training. It's super jacked."""
    X_train = []
    y_train = []
    # Loop through our batch and create arrays for X and y
    # so that we can fit our model at every step.
    for memory in minibatch:
        # Get stored values.
        old_state_m, action_m, reward_m, new_state_m = memory

        print("old_state_m:")
        print(old_state_m)
        print('---------------------------')
        print("action_m:")
        print(action_m)
        print('---------------------------')
        print("reward_m:")
        print(reward_m)
        print('---------------------------')
        print("new_state_m:")
        print(new_state_m)
        print('---------------------------')
        # Get prediction on old state.
        old_qval = model.predict(old_state_m, batch_size=1)
        #print("OLD QVAL:")
        #print(old_qval)
        #print('---------------------------')
        # Get prediction on new state.
        newQ = model.predict(new_state_m, batch_size=1)
        #print("NEW QVAL:")
        #print(newQ)
        #print('---------------------------')
        # Get our best move. I think?
        maxQ = np.max(newQ)
        #print("MAX QVAL:")
        #print(maxQ)
        #print('---------------------------')
        y = np.zeros((1, NUM_INPUT))
        y[:] = old_qval[:]
        # Check for terminal state.
        if reward_m != -5000:  # non-terminal state
            update = (reward_m + (GAMMA * maxQ))
        else:  # terminal state
            update = reward_m
        # Update the value for the action we took.
        y[0][action_m] = update
        X_train.append(old_state_m.reshape(NUM_INPUT,))
        y_train.append(y.reshape(NUM_INPUT,))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train


def params_to_filename(params):
    return str(params['nn'][0]) + '-' + str(params['nn'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])


def launch_learn(params):
    filename = params_to_filename(params)
    print("Trying %s" % filename)
    # Make sure we haven't run this one.
    if not os.path.isfile('results/sonar-frames/loss_data-' + filename + '.csv'):
        # Create file so we don't double test when we run multiple
        # instances of the script at the same time.
        open('results/sonar-frames/loss_data-' + filename + '.csv', 'a').close()
        print("Starting test.")
        # Train.
        model = neural_net(NUM_INPUT, params['nn'])
        train_net(model, params)
    else:
        print("Already tested.")


if __name__ == "__main__":
    if TUNING:
        print(1)
        param_list = []
        nn_params = [[164, 150], [256, 256],
                     [512, 512], [1000, 1000]]
        batchSizes = [40, 100, 400]
        buffers = [10000, 50000]

        for nn_param in nn_params:
            for batchSize in batchSizes:
                for buffer in buffers:
                    params = {
                        "batchSize": batchSize,
                        "buffer": buffer,
                        "nn": nn_param
                    }
                    param_list.append(params)

        for param_set in param_list:
            launch_learn(param_set)

    else:
        print(2)
        nn_param = [164, 150]
        params = {
            "batchSize": 5,
            "buffer": 5000,
            "nn": nn_param
        }
        model = neural_net(NUM_INPUT, nn_param,False)
        train_net(model, params)

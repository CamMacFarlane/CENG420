"""
The design of this comes from here:
http://outlace.com/Reinforcement-Learning-Part-3/
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))



def neural_net(num_sensors, params, load=False):
    model = Sequential()

    # First layer.
    #param = [164, 150]
    model.add(Dense(164, kernel_initializer='lecun_uniform', input_shape=(num_sensors,) ))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    # Second layer.
    model.add(Dense(150, kernel_initializer='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    # Output layer.
    model.add(Dense(num_sensors, kernel_initializer='lecun_uniform'))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    if load:
        model.load_weights('saved-models/weight.h5')

    return model


def lstm_net(num_sensors, load=False):
    model = Sequential()
    model.add(LSTM(
        output_dim=512, input_dim=num_sensors, return_sequences=True
    ))
    model.add(Dropout(0.2))
    model.add(LSTM(output_dim=512, input_dim=512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=3, input_dim=512))
    model.add(Activation("linear"))
    model.compile(loss="mean_squared_error", optimizer="rmsprop")

    return model

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input


def weights_size(layers):
    s = 0
    for i in range(len(layers)-1):
        s += layers[i] * layers[i+1]
    return s


class Model:
    # input layer 4 directions of dangers * 4 directions of movement * 4 directions of food
    # output layer 4 directions of movement
    def __init__(self, layers=[12, 120, 120, 120, 4]):
        self.layers = layers
        self.nb_weights = weights_size(layers)
        self.state_size = layers[0]

    def build_model(self, weights):
        if len(self.layers) < 2:
            print("Error: A model has to have at least 2 layers (input and output layer)")
            return None
        model = Sequential()
        added_weights = 0
        nb_layers = len(self.layers)  # considering input layer and first hidden layer are created at the same time
        model.add(Input(shape=(self.layers[0],)))
        for i in range(1, nb_layers):
            activation = 'relu'
            if i == nb_layers-1:
                activation = 'softmax'
            model.add(Dense(units=self.layers[i], activation=activation))
            weight = weights[added_weights:added_weights+self.layers[i-1]*self.layers[i]].reshape(self.layers[i-1], self.layers[i])
            added_weights += self.layers[i-1]*self.layers[i]
            model.layers[-1].set_weights((weight, np.zeros(self.layers[i])))
        return model

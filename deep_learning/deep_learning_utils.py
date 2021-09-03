import sys
sys.path.append("C:/Users/voyno/Desktop/finance")

from data import data_utils
import matplotlib.pyplot as plt

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout


def build_nn(input_shape=None, num_layers=6, nodes=64, activation='relu', output="classification", dropout=False, dropout_prob=.25):
    
    # model architecture
    input_layer = Dense(nodes, activation=activation, input_shape=input_shape)
    layers = [Dense(nodes, activation=activation) for i in range(num_layers-2)]
    if output == "classification":
        output_layer = Dense(1, activation="sigmoid")
    else:
        output_layer = Dense(1, activation="linear")

    # concatenating layer segments
    layers = [input_layer] + layers + [output_layer]

    layers_with_dropout = []
    if dropout:
        for i in range(len(layers) - 1):
            layers_with_dropout.append(layers[i])
            layers_with_dropout.append(Dropout(dropout_prob))
        layers_with_dropout.append(layers[-1])
        layers = layers_with_dropout
        
    # create model and compile
    model = Sequential(layers)
    if output == "classification":
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    else:
        model.compile(loss='mse', optimizer='adam')
    
    return model


def train_nn(model, x_train, y_train, test, epochs=20, batch_size=2048):
    
    history = model.fit(
        x_train,
        y_train, 
        epochs=epochs, 
        batch_size=batch_size, 
        validation_data=test)
    
    return history


def run_classifier(data):
    
    # Convert prices to percent change
    raw_data = data["Adj Close"].pct_change().values[1:]

    # Clean and transform data for modeling
    sequences = data_utils.clean_data(raw_data)
    train_sequences, test_sequences = data_utils.train_test_split(sequences)

    # slice sequences for input-output relationtip with lagged price data as input
    x_train, y_train = data_utils.slice_sequences(train_sequences, classification=True)
    x_test, y_test = data_utils.slice_sequences(test_sequences, classification=True)
    print("\nNumber Train Sequences: {}\ttotal data: {}".format(len(train_sequences), x_train.shape[0])) 
    print("Number Test Sequences: {}\ttotal data: {}\n".format(len(test_sequences), x_test.shape[0])) 
    
    # Basic neural net using custom deep learning utils
    model = build_nn(input_shape=x_train.shape[1:], dropout=True)
    history = train_nn(model, x_train, y_train, (x_test, y_test))
    
    return history

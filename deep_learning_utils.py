from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


def build_nn(input_shape=None, num_layers=6, nodes=64, activation='relu', output="classification"):
        
    input_layer = Dense(nodes, activation=activation, input_shape=input_shape)
    layers = [Dense(nodes, activation=activation) for i in range(num_layers-2)]
    output_layer = Dense(1, activation="sigmoid")
    
    layers = [input_layer] + layers + [output_layer]
        
    # create model and compile
    model = Sequential(layers)
    if output == "classification":
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    else:
        model.compile(loss='mse', optimizer='adam')
    
    print(model.summary())
    
    return model


def train_nn(model, x_train, y_train, test, epochs=10, batch_size=1024):
    
    history = model.fit(
        x_train,
        y_train, 
        epochs=epochs, 
        batch_size=batch_size, 
        validation_data=test)
    
    return history
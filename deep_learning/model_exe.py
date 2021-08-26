import data_utils
import deep_learning_utils
import matplotlib.pyplot as plt

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
    model = deep_learning_utils.build_nn(input_shape=x_train.shape[1:], dropout=True)
    history = deep_learning_utils.train_nn(model, x_train, y_train, (x_test, y_test))
    
    return history
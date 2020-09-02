import numpy as np
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
import keras
from keras.layers import Dense
from keras.models import Sequential

#==============================================================================
# Input
#==============================================================================
input_data = [np.array([0, 3]), np.array([1, 2]), np.array([-1, -2]), np.array([4, 0])]
weights_0 = {'node_0' : np.array([2, 1]),
           'node_1' : np.array([1, 2]),
           'output' : np.array([1, 1])
           }

weights_1 = {'node_0' : np.array([2, 1]),
           'node_1' : np.array([1.0, 1.5]),
           'output' : np.array([1.0, 1.5])
           }

target_actuals = [1, 3, 5, 7]

target = 0
learning_rate = 0.01

#==============================================================================
# Function
#==============================================================================
# Activation Function
def relu(input): 
    return(max(0, input))

# Function to Get First HIDDEN LAYER
def fFlt_predictOutput(l_inputData, l_weight, str_function = 'Identity'):
    l_Output = (l_inputData * l_weight).sum()
    return(l_Output)
    
# Function to Get output with 1 HIDDEN LAYER
def fFlt_predict_with_network(l_inputData, d_weight):
    # Calculate node 0 value
    node_0_input = (l_inputData * d_weight['node_0']).sum()
    node_0_output = relu(node_0_input)
    # Calculate node 1 value
    node_1_input = (l_inputData * d_weight['node_1']).sum()
    node_1_output = relu(node_1_input)
    # Put node values into array: hidden_layer_outputs
    hidden_layer_values = np.array([node_0_output, node_1_output])
    # Calculate model output
    input_to_final_layer = (hidden_layer_values * d_weight['output']).sum()
    model_output = relu(input_to_final_layer)
    return(model_output)
    
def fFlt_meanSquaredError(l_seriesOfOutput, l_seriesOfPrevision):
    return metrics.mean_squared_error(l_seriesOfOutput, l_seriesOfPrevision)

def get_slope(l_input_data, flt_target, l_weights):
    flt_preds = (l_weights * l_input_data).sum()
    flt_error = flt_preds - flt_target
    l_slope = 2 * l_input_data * flt_error
    return l_slope

def get_mse(l_input_data, flt_target, l_weights):
    flt_modelOutput = fFlt_predictOutput(l_input_data, l_weights)
    flt_mse = fFlt_meanSquaredError([flt_modelOutput], [flt_target])
    return flt_mse
    


#==============================================================================
# Last Code
#==============================================================================

# predictors = matrix of df without wage_per_hour
# target = matrix of df only with wage_per_hour

# Save the number of columns in predictors: n_cols
n_cols = predictors.shape[1]

# Set up the model: model
model = Sequential()

# Add the first layer
model.add(Dense(50, activation='relu', input_shape=(n_cols,)))
model.add(Dense(32, activation='relu')) # Add the second layer
model.add(Dense(1))                     # Add the output layer












## Course 1
## Forward Propagation Code - Get the the first Node (HIDDEN LAYER)
#node_0_value = (input_data * weights['node_0']).sum()
#node_1_value = (input_data * weights['node_1']).sum()
#hidden_layer_values = np.array([node_0_value, node_1_value])
## Forward Propagation Code - Get the ouput
#model_output = (hidden_layer_values * weights['output']).sum()
#print(model_output)

#----------------------------------------------------------------

## Course 2
## Activation Function
#def relu(input):
#    output = max(0, input)
#    return(output)
#node_0_input = (input_data * weights['node_0']).sum()
#node_1_input = (input_data * weights['node_1']).sum()
#node_0_output = relu(node_0_input)
#node_1_output = relu(node_1_input)
#hidden_layer_values = np.array([node_0_output, node_1_output])
#model_output = (hidden_layer_values * weights['output']).sum()
#print(model_output)

#----------------------------------------------------------------

## Course 4
## Multi-layer neural networks
#def predict_with_network(input_data):
#    # Calculate node 0 in the first hidden layer
#    node_0_0_input = (input_data * weights['node_0_0']).sum()
#    node_0_0_output = relu(node_0_0_input)
#    # Calculate node 1 in the first hidden layer
#    node_0_1_input = (input_data * weights['node_0_1']).sum()
#    node_0_1_output = relu(node_0_1_input)
#    # Put node values into array: hidden_0_outputs
#    hidden_0_outputs = np.array([node_0_0_output, node_0_1_output])
#    # Calculate node 0 in the second hidden layer
#    node_1_0_input = (hidden_0_outputs * weights['node_1_0']).sum()
#    node_1_0_output = relu(node_1_0_input)
#    # Calculate node 1 in the second hidden layer
#    node_1_1_input = (hidden_0_outputs * weights['node_1_1']).sum()
#    node_1_1_output = relu(node_1_1_input)
#    # Put node values into array: hidden_1_outputs
#    hidden_1_outputs = np.array([node_1_0_output, node_1_1_output])
#    # Calculate model output: model_output
#    model_output = (hidden_1_outputs * weights['output']).sum()
#    # Return model_output
#    return(model_output)
#output = predict_with_network(input_data)
#print(output)


#----------------------------------------------------------------

## Course 2.1
## Compare 2 set of Weight ==> Get the most precise
## List to 0
#model_output_0 = []
#model_output_1 = []
## Loop over input_data
#for row in input_data:
#    # Append prediction to model_output_0
#    model_output_0.append(predict_with_network(row, weights_0))
#    # Append prediction to model_output_1
#    model_output_1.append(predict_with_network(row, weights_1))
## Calculate the mean squared error for both model
#mse_0 = metrics.mean_squared_error(model_output_0, target_actuals)
#mse_1 = metrics.mean_squared_error(model_output_1, target_actuals)
## Print mse_0 and mse_1
#print("Mean squared error with weights_0: %f" %mse_0)
#print("Mean squared error with weights_1: %f" %mse_1)


#----------------------------------------------------------------

## Course 2.2
## Calculate the slope ==> Update Weight accordingly
## Set the learning rate: learning_rate
#learning_rate = 0.01
## Calculate the predictions: preds
#preds = (weights * input_data).sum()
## Calculate the error: error
#error = preds - target
## Calculate the slope: slope
#slope = 2 * input_data * error
## Update the weights: weights_updated
#weights_updated = weights - (learning_rate*slope)
## Get updated predictions: preds_updated
#preds_updated = (weights_updated * input_data).sum()
## Calculate updated error: error_updated
#error_updated = preds_updated - target
## Print the original error
#print(error)
#print(error_updated)

#----------------------------------------------------------------

## Course 2.3
#mse_hist = []
## Iterate over the number of updates
#for i in range(20):
#    # Calculate the slope: slope
#    slope = get_slope(input_data, target, weights)
#    # Update the weights: weights
#    weights = weights - learning_rate * slope
#    # Calculate mse with new weights: mse
#    mse = get_mse(input_data, target, weights)
#    # Append the mse to mse_hist
#    mse_hist.append(mse)
## Plot the mse history
#plt.plot(mse_hist)
#plt.xlabel('Iterations')
#plt.ylabel('Mean Squared Error')
#plt.show()


#----------------------------------------------------------------

## Course 3.1
## KERAS Model



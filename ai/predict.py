import os
import numpy as np

# with open(os.path.join('ai', 'classes.txt'), 'r') as desc:
#     # Split string read on whitespace
#     classes = desc.read().split()
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def predict(pattern, model, box_size=32):

    # Reshape from flattened to box
    pattern = pattern.reshape((box_size, box_size, 1))

    # Predict probabilities
    one_hot = model.predict([pattern])[0] # Predict
    # Get index of the highest probability
    index = np.argmax(one_hot)

    return classes[index]

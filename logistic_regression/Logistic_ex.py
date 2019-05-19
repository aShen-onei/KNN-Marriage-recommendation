from sklearn.linear_model import logistic
import numpy as np
import random

def sigmoid(inX):
    return 1.0/(1+np.exp(-inX))

def randomAscent(data)
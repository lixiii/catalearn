# Catalearn

### Easy and affordable machine learning on cloud GPUs

## Intro

The Catalearn module aims to provide access to fast GPUs for those interested in working on machine learning projects but don't have the resources to buy their own GPU. 

AWS GPU instances are great, but they take quite some time to set up. And since they charge by the hour, you would end up paying for a lot more time than the time you spend training the model.

This is where catalearn comes in, simply upload your code and data with the module, and it will handle the rest. We are still beta testing so everything is __completely free__.

## Installation
`pip3 install git+https://github.com/Catalearn/catalearn`

## Note: Currently it only works with python3 and only supports the Tensorflow and Keras frameworks

## Usage
API: `catalearn.run(function, *args)`
```
import catalearn
def func(data1, data2):
    # define model and train
    return model

catalearn.run(func, data1, data2)
```

## Example: Training a CNN on the MNIST dataset
### Dependencies: __catalearn__, __keras__ and __pandas__
```
from keras.datasets import mnist
import catalearn
import pandas as pd

# Prepare the dataset

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train_reshape = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test_reshape = x_test.reshape(x_test.shape[0], 28, 28, 1)

y_train_onehot = pd.get_dummies(y_train).as_matrix()
y_test_onehot = pd.get_dummies(y_test).as_matrix()


# Put all the code you want to run on the GPU inside a function
# NOTE: The model should be defined inside the function, otherwise it might cause errors

def train_on_gpu(x_train_reshape, y_train_onehot, x_test_reshape, y_test_onehot):

    # Define the model

    from keras.models import Sequential
    from keras.layers import Dense, Activation, Conv2D, Flatten, MaxPooling2D

    model = Sequential()

    model.add(Conv2D(32, (3, 3), input_shape=(28, 28, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3)))
    model.add(Flatten())
    model.add(Activation('relu'))
    model.add(Dense(units=10))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='Adadelta', metrics=['accuracy'])

    # train the model

    model.fit(x_train_reshape, y_train_onehot, epochs=5, batch_size=32)

    loss_and_metrics = model.evaluate(x_test_reshape, y_test_onehot, batch_size=128)
    print("\n\n Trained model has test accuracy {0}".format(loss_and_metrics[1]))

    return model


# use Catalearn to run on a cloud GPU

model = catalearn.run(train_on_gpu, x_train_reshape, y_train_onehot, x_test_reshape, y_test_onehot)

print(model)
# output should be similar to 
# <keras.models.Sequential object at 0x110badc18>
```

## __Common Problems__

1. Tensor must be from the same graph

__Error:__ `ValueError: Tensor("mul_3:0", shape=(32,), dtype=float32) must be from the same graph as Tensor("mul:0", shape=(32,), dtype=float32).`

__Solution:__ Move all code related to the model inside the GPU function, only do data preprocessing locally.

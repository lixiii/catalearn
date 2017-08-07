# Catalearn

## Run your code on a GPU with zero setup

__Catalearn__ is a jupyter notebook plugin that allows you to easily run your code on a GPU. You can simply add a one line magic to your cell and it will automatically be run on a cloud GPU. 

## Installation
1. First install Jupyter Notebook
2. Install Catalearn with the following command
`sudo pip3 install git+https://github.com/yl573/catalearn`

## Update
1. `sudo pip3 uninstall catalearn`
2. `sudo pip3 install git+https://github.com/yl573/catalearn`

## How it works
Catalearn can be used through its cell magic `%%catalearn`. The syntax is a follows:
`%%catalearn <YOUR_API_KEY>`
Where `<YOUR_API_KEY>` is the api key given to you for beta testing

## EXAMPLE
Run the code below inside a jupyter cell, replacing `<YOUR_API_KEY>` with the key you were given
```
%%catalearn <YOUR_API_KEY>

from keras.datasets import mnist
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, Flatten, MaxPooling2D

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train_reshape = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test_reshape = x_test.reshape(x_test.shape[0], 28, 28, 1)

y_train_onehot = pd.get_dummies(y_train).as_matrix()
y_test_onehot = pd.get_dummies(y_test).as_matrix()

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3)))
model.add(Flatten())
model.add(Activation('relu'))
model.add(Dense(units=10))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='Adadelta', metrics=['accuracy'])
model.fit(x_train_reshape, y_train_onehot, epochs=5, batch_size=32)

loss_and_metrics = model.evaluate(x_test_reshape, y_test_onehot, batch_size=512)
print("\n\nTrained model has test accuracy {0}".format(loss_and_metrics[1]))

del x_train_reshape, x_test_reshape, y_train_onehot, y_test_onehot
```
You can then use the model in the next cell
```
print(loss_and_metrics)
print(model)
```


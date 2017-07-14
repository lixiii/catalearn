from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, Flatten, MaxPooling2D
import pandas as pd
import catalearn
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("Before reshaping:\n")
print("x_train has shape {0}".format(x_train.shape))
print("x_test has shape {0}".format(x_test.shape))
x_train_reshape = x_train.reshape(x_train.shape[0], 28, 28, 1)#[:1000]
x_test_reshape = x_test.reshape(x_test.shape[0], 28, 28, 1)#[:200]
print("\nAfter reshaping:\n")
print("x_train_reshape has shape {0}".format(x_train_reshape.shape))
print("x_test_reshape has shape {0}".format(x_test_reshape.shape))

y_train_onehot = pd.get_dummies(y_train).as_matrix()#[:1000]
y_test_onehot = pd.get_dummies(y_test).as_matrix()#[:200]
print("Onehot encoding converts {0} into {1}".format(y_train[0], y_train_onehot[0]))

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3)))
model.add(Flatten())
model.add(Activation('relu'))
model.add(Dense(units=10))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='Adadelta', metrics=['accuracy'])

model.fit(x_train_reshape, y_train_onehot, epochs=1, batch_size=32)

loss_and_metrics = model.evaluate(x_test_reshape, y_test_onehot, batch_size=128)
print("\n\n Trained model has test accuracy {0}".format(loss_and_metrics[1]))

model.save('./model.hdf5')
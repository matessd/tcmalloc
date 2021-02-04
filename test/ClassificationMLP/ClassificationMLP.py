import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

print(f'tensorflow version: {tf.__version__}')
print(f"keras version: {keras.__version__}")

# from sklearn.datasets import load_iris
# from sklearn.linear_model import Perceptron
#
# iris = load_iris()
# X = iris.data[:, (2, 3)]   # petal length, petal width
# y = (iris.target == 0).astype(np.int)
#
# per_clf = Perceptron()
# per_clf.fit(X, y)
# print(per_clf)

fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

# print(X_train_full.shape)  # (60000, 28, 28)
X_valid, X_train = X_train_full[ :5000 ] / 255.0, X_train_full[ 5000: ] / 255.0
y_valid, y_train = y_train_full[ :5000 ], y_train_full[ 5000: ]

class_names = [ "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
                "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot" ]
# print(class_names[ y_train[ 0 ] ])
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[ 28, 28 ]),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dense(200, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

# print(model.summary())
# print(model.layers[2].name)
# print(model.get_layer('dense_3').name)

# weights, biases = model.layers.get_weights()

# print(weights.shape)
# print()

# Compiling the Model
model.compile(loss="sparse_categorical_crossentropy",
              optimizer="sgd",
              metrics=[ "accuracy" ])

# fit part
history = model.fit(X_train, y_train, epochs=10,
                    validation_data=(X_valid, y_valid))

# plot part
pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

# evaluate on the test set to estimate the generalization error before deploy the model
print(model.evaluate(X_test, y_test))

# predict
X_new = X_test[: 3]
y_proba = model.predict(X_new)
print(y_proba.round(2))  # predict probability of each class (10 class)

# predict which class
y_pred = model.predict_classes(X_new)
print(f"y_pred class is {y_pred}")  # which class has the highest probability
print(np.array(class_names)[y_pred])  # class name

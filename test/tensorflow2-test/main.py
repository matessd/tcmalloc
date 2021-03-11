import os
# forbidden gpu
os.environ["CUDA_VISIBLE_DEVICES"]="-1" 
import numpy as np
#import pandas as pd
import tensorflow as tf
#import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import gc
import multiprocessing
import time

def ClassificationMLP():
    print(f'tensorflow version: {tf.__version__}')
    print(f"keras version: {keras.__version__}")

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

    # Compiling the Model
    model.compile(loss="sparse_categorical_crossentropy",
                optimizer="sgd",
                metrics=[ "accuracy" ])

    # fit part
    history = model.fit(X_train, y_train, epochs=3,
                        validation_data=(X_valid, y_valid))

    # plot part
    #pd.DataFrame(history.history).plot(figsize=(8, 5))
    #plt.grid(True)
    #plt.gca().set_ylim(0, 1)
    #plt.show()

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

def RegressionMLP():
    housing = fetch_california_housing()

    X_train_full, X_test, y_train_full, y_test = train_test_split(housing.data, housing.target)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_valid_scaled = scaler.transform(X_valid)
    X_test_scaled = scaler.transform(X_test)

    model = keras.models.Sequential([
        keras.layers.Dense(30, activation="relu", input_shape=X_train.shape[1:]),
        keras.layers.Dense(1)
    ])
    model.compile(loss="mean_squared_error", optimizer="sgd")
    history = model.fit(X_train, y_train, epochs=25,
                        validation_data=(X_valid, y_valid))
    mse_test = model.evaluate(X_test, y_test)
    X_new = X_test[:3]  # pretend these  are new instances
    y_pred = model.predict(X_new)

#p = multiprocessing.Process(target=ClassificationMLP)
#p.start()
#p.join()
for i in range(3):
    ClassificationMLP()
    gc.collect()
    RegressionMLP()
    gc.collect()
timeout = time.time() + 16
while True:
    if time.time()>timeout:
        break

from __future__ import print_function
import keras
from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
import pandas as pd
import pickle

batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
spect_rows, spect_cols = 128, 2584

img_rows, img_cols = 28, 28

(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

# import mel spectrogram data
spectral_analysis = pickle.load(open("spectral_analysis.pkl", "rb"))

# sort out train and test data
x_train_rows = [row for row in spectral_analysis if row['type'] == 'Dev']
x_test_rows = [row for row in spectral_analysis if row['type'] == 'Test']

# stack spectrograms side by side
x_train = np.array([np.hstack((row['bass spect'], row['drums spect'], row['other spect'], row['vocals spect'])) for row in x_train_rows])
x_test = np.array([np.hstack((row['bass spect'], row['drums spect'], row['other spect'], row['vocals spect'])) for row in x_test_rows])

# reshape data
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# import output (level anaylsis) data
level_analysis = pd.read_csv("level_analysis.csv")

# sort out train and test data
y_train_rows = level_analysis.loc[level_analysis['type'] == 'Dev']
y_test_rows = level_analysis.loc[level_analysis['type'] == 'Test']

# crate array of length 4 arrays
y_train = np.array([np.array([row[1]['bass ratio'], row[1]['drums ratio'], row[1]['other ratio'], row[1]['vocals ratio']]) for row in y_train_rows.iterrows()])
y_test = np.array([np.array([row[1]['bass ratio'], row[1]['drums ratio'], row[1]['other ratio'], row[1]['vocals ratio']]) for row in y_test_rows.iterrows()])



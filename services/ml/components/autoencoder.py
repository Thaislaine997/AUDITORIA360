from tensorflow import keras
import numpy as np

def build_autoencoder(input_dim):
    input_layer = keras.layers.Input(shape=(input_dim,))
    encoded = keras.layers.Dense(16, activation='relu')(input_layer)
    decoded = keras.layers.Dense(input_dim, activation='linear')(encoded)
    autoencoder = keras.Model(input_layer, decoded)
    autoencoder.compile(optimizer='adam', loss='mse')
    return autoencoder

def train_autoencoder(model, X: np.ndarray, epochs=20, batch_size=32):
    model.fit(X, X, epochs=epochs, batch_size=batch_size, verbose=0)
    return model

def predict_reconstruction_error(model, X: np.ndarray):
    recon = model.predict(X)
    return np.mean(np.square(X - recon), axis=1)

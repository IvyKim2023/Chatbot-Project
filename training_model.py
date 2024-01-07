from preprocessing import num_encoder_tokens, num_decoder_tokens, decoder_target, encoder_input, decoder_input, decoder_target, input_dict, max_encoder_seq_len
from tensorflow import keras
from keras.layers import Input, LSTM, Dense
from keras.models import Model
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Choose dimensionality
dimensionality = 256

# Choose the batch size and number of epochs
# Usually, with greater epochs the model can perform better
# However, it will take much longer to run if we run it on a CPU
batch_size = 10
epochs = 1000

# Encoder training setup
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder_lstm = LSTM(dimensionality, return_state=True)
encoder_outputs, state_hidden, state_cell = encoder_lstm(encoder_inputs)
encoder_states = [state_hidden, state_cell]

# Decoder training setup
decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(dimensionality, return_sequences=True, return_state=True)
decoder_outputs, decoder_state_hidden, decoder_state_cell = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Building the training model
training_model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile the model
training_model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'], sample_weight_mode='temporal')

# Train the model
training_model.fit([encoder_input, decoder_input], decoder_target, batch_size = batch_size, epochs = epochs, validation_split = 0.2)

# Save the model
training_model.save('trained_model.h5')

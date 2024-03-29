from preprocessing import target_dict, reverse_target_dict, max_decoder_seq_len
from training_model import decoder_inputs, decoder_lstm, decoder_dense, num_decoder_tokens, num_encoder_tokens, input_dict, max_encoder_seq_len
from tensorflow import keras
from keras.layers import Input
from keras.models import Model, load_model
import numpy as np

training_model = load_model('trained_model.h5')
encoder_inputs = training_model.input[0]
encoder_outputs, state_h_enc, state_c_enc = training_model.layers[2].output
encoder_states = [state_h_enc, state_c_enc]
encoder_model = Model(encoder_inputs, encoder_states)

latent_dim = 256
decoder_state_input_hidden = Input(shape=(latent_dim,))
decoder_state_input_cell = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_hidden, decoder_state_input_cell]
decoder_outputs, state_hidden, state_cell = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_hidden, state_cell]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

def decode_sequence(test_input):
  # Encode the input as state vectors.
  states_value = encoder_model.predict(test_input)

  # Generate empty target sequence of length 1.
  target_seq = np.zeros((1, 1, num_decoder_tokens))
  # Populate the first token of target sequence with the start token.
  target_seq[0, 0, target_dict['<START>']] = 1.

  # Sampling loop for a batch of sequences
  decoded_sentence = ''

  stop_condition = False
  while not stop_condition:
    # Run the decoder model to get possible output tokens (with probabilities) & states
    output_tokens, hidden_state, cell_state = decoder_model.predict(
      [target_seq] + states_value)

    # Choose token with highest probability
    sampled_token_index = np.argmax(output_tokens[0, -1, :])
    sampled_token = reverse_target_dict[sampled_token_index]
    decoded_sentence += " " + sampled_token

    # Exit condition: either hit max length or find stop token
    if (sampled_token == '<END>' or len(decoded_sentence) > max_decoder_seq_len):
      stop_condition = True

    # Update the target sequence 
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    target_seq[0, 0, sampled_token_index] = 1.

    # Update states
    states_value = [hidden_state, cell_state]

  return decoded_sentence
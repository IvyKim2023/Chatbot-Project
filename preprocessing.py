import numpy as np
import re
from dialogue_pair_up import pairs

# Build empty lists to hold input and target lines
input_lines = []
target_lines = []

# Build empty token sets
input_tokens = set()
target_tokens = set()

# Choose how many dialogues from the txt file we want to use to train the model
for line in pairs[:1000]:
  # Get each input and target line from the pair
  input_line, target_line = line[0], line[1]
  # Split words from punctuation  
  input_line = " ".join(re.findall(r"[\w']+|[^\s\w]", input_line))
  target_line = " ".join(re.findall(r"[\w']+|[^\s\w]", target_line))
  # Append the input line to input lines list
  input_lines.append(input_line)
  # Add '<START> ' and ' <END>'
  target_line = '<START> ' + target_line + ' <END>'
  # Append the target line to target lines list
  target_lines.append(target_line)
  
  # Add the tokens to each set
  for token in input_line.split():
    if token not in input_tokens:
      input_tokens.add(token)
  for token in target_line.split():
    if token not in target_tokens:
      target_tokens.add(token)

# Sort the token sets
input_tokens = sorted(list(input_tokens))
target_tokens = sorted(list(target_tokens))

# Get the number of tokens of encoder and decoder
num_encoder_tokens = len(input_tokens)
num_decoder_tokens = len(target_tokens)

# Get the maximum length of a line
max_encoder_seq_len = max([len(re.findall(r"[\w']+|[^\s\w]", input_line)) for input_line in input_lines])
max_decoder_seq_len = max([len(re.findall(r"[\w']+|[^\s\w]", target_line)) for target_line in target_lines])

# Build the input and output dictionaries for later use
input_dict = dict([(token, i) for i, token in enumerate(input_tokens)])
target_dict = dict([(token, i) for i, token in enumerate(target_tokens)])

# Build the reversed input and output dictionaries
reverse_input_dict = dict((i, token) for token, i in input_dict.items())
reverse_target_dict = dict((i, token) for token, i in target_dict.items())

# Create empty matrices for encode input, decode input, and decode output
encoder_input = np.zeros((len(input_lines), max_encoder_seq_len, num_encoder_tokens), dtype='float32')
decoder_input = np.zeros((len(input_lines), max_decoder_seq_len, num_decoder_tokens), dtype='float32')
decoder_target = np.zeros((len(input_lines), max_decoder_seq_len, num_decoder_tokens), dtype='float32')

# Assign the 1s
for idx, (input_line, target_line) in enumerate(zip(input_lines, target_lines)):
  for timestep, token in enumerate(re.findall(r"[\w']+|[^\s\w]", input_line)):
    encoder_input[idx, timestep, input_dict[token]] = 1.
  for timestep, token in enumerate(target_line.split()):
    decoder_input[idx, timestep, target_dict[token]] = 1.
    if timestep > 0:
      decoder_target[idx, timestep - 1, target_dict[token]] = 1.
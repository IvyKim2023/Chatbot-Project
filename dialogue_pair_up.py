from itertools import zip_longest

# Get the cleaned dialogues
dialogue_path = "______________"

# Split the lines
with open(dialogue_path, 'r', encoding='utf-8') as f:
  lines = f.read().split('\n')

# Pair up the lines
def grouper(dialogue_lines, n, fillvalue=None):
    args = [iter(dialogue_lines)] * n
    return zip_longest(*args, fillvalue=fillvalue)

# If the number of lines is odd, just add a response 'Cool\n'
pairs = list(grouper(lines, 2, 'Cool!\n'))

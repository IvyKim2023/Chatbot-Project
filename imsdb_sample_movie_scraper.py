import requests
from bs4 import BeautifulSoup
import os

download_path = r'______'  # Set download path
os.chdir(download_path)

# URL of the movie script on IMSDb
url = 'https://imsdb.com/scripts/________.html'

# Send a request to the URL
response = requests.get(url)
data = response.text

# Parse the HTML content
soup = BeautifulSoup(data, 'html.parser')

# Extract script text
script_text = soup.find('pre').get_text()

# Process the script_text to isolate dialogues but still with character names and spaces
script_text = os.linesep.join([line for line in script_text.splitlines() if line.startswith('                       ')])
script_text = os.linesep.join([line for line in script_text.splitlines() if line.strip() != ''])
script_text = os.linesep.join(
    [line for line in script_text.splitlines() 
     if (line.startswith('                       ') and len(line) > 23 and line[23] != ' ') 
     or (line.startswith('                                   ') and len(line) > 35 and line[35] != ' ')]
)

# Turn the dialogues into lines instead of blocks and delete the character names
# Determine if a line is just the character's name by the spacing format
def is_character_name(line):
    return line.startswith('                                   ') and len(line) > 35 and line[35] != ' '

# Create a list to have the processed dialogues and a list to have the parts of dialogue that is being processed
dialogue_lines = []
current_dialogue = []

for line in script_text.splitlines():
    if line.strip() == "": continue
    if not is_character_name(line):
        current_dialogue.append(line.strip().rstrip('\n'))
    else:
        if current_dialogue:
            dialogue_lines.append(' '.join(current_dialogue))
            current_dialogue = []

#print(dialogue_lines)
            
# Change script_text to the content of the dialogue_lines
script_text = os.linesep.join(dialogue_lines)

# Clean the blank lines
script_lines = script_text.split('\n')
cleaned_script = [line.strip() for line in script_lines if line.strip()]
cleaned_script_text = '\n'.join(cleaned_script)

# Write processed dialogues to a file
with open('____.txt', 'w') as file:
    file.write(cleaned_script_text)
    

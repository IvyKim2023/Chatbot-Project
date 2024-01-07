import numpy as np
import requests
import re
from test_model import encoder_model, decoder_model, num_decoder_tokens, num_encoder_tokens, input_dict, target_dict, reverse_target_dict, max_decoder_seq_len, max_encoder_seq_len

class ChatBot:

  # Aswer the weather
  def get_weather(self, city):
        key = "__________"  # OpenWeatherMap API Key
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?" + "appid=" + key + "&q=" + city + "&units=metric")
        weather_data = response.json()
        if weather_data['cod'] != '404':
            main_data = weather_data['main']
            temperature = main_data['temp']
            pressure = main_data['pressure']
            humidity = main_data['humidity']
            weather_description = weather_data['weather'][0]['description']
            return (f"City: {city}\n         Temperature: {temperature}°C\n         Pressure: {pressure} hPa\n         Humidity: {humidity}%\n         Description: {weather_description.capitalize()}")
        else:
            return "City not found."
    
  def string_to_matrix(self, user_input):
    tokens = re.findall(r"[\w']+|[^\s\w]", user_input)
    user_input_matrix = np.zeros(
      (1, max_encoder_seq_len, num_encoder_tokens),
      dtype='float32')
    for timestep, token in enumerate(tokens):
      if token in input_dict:
        user_input_matrix[0, timestep, input_dict[token]] = 1.
    return user_input_matrix
  
  # Get the response with the user input
  def generate_response(self, user_input):
    input_matrix = self.string_to_matrix(user_input)
    states_value = encoder_model.predict(input_matrix)
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    target_seq[0, 0, target_dict['<START>']] = 1.
    
    # The rest is the same as decode_sequence() in test_model.py 
    # because basically the chatbot_response is decoded_sentence
    chatbot_response = ''

    stop_condition = False
    while not stop_condition:
      output_tokens, hidden_state, cell_state = decoder_model.predict(
        [target_seq] + states_value)
      
      sampled_token_index = np.argmax(output_tokens[0, -1, :])
      sampled_token = reverse_target_dict[sampled_token_index]
      
      chatbot_response += " " + sampled_token
      
      if (sampled_token == '<END>' or len(chatbot_response) > max_decoder_seq_len):
        stop_condition = True
        
      target_seq = np.zeros((1, 1, num_decoder_tokens))
      target_seq[0, 0, sampled_token_index] = 1.
      
      states_value = [hidden_state, cell_state]
      
    chatbot_response = chatbot_response.replace("<START>", "").replace("<END>", "") + "\n"
      
    return chatbot_response
  



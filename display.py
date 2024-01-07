import tkinter as tk
from chatbot import ChatBot  

chatbot = ChatBot()

# Define the exit_commands
exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "stop")

# Create the background window
background = tk.Tk()
background.title("Chatbot") 
background.geometry("700x600")  

# Show the chat record
chat_history = tk.Text(background, height=30, width=80)  
chat_history.pack(pady=15)  

instruction = tk.Label(background, text="Chat with the Chatbot from here:")
instruction.pack() 

# Create the user input bar
user_input = tk.Entry(background, width=80)  
user_input.pack()  

# Prepare for it if the user ask about the weather
if_weather = False


def chat(event = None):  
    global exit_commands
    global if_weather

    user_message = user_input.get()  
    chat_history.insert(tk.END, "Me: " + user_message + "\n")  

    # if the user ask about the weather
    if if_weather == True:
        city = user_input.get()
        weather_response = chatbot.get_weather(city)
        user_input.delete(0, tk.END)
        chat_history.see(tk.END)
        chat_history.insert(tk.END, "Chatbot: " + weather_response + "\n")
        if_weather = False
    else:
        if "weather" in user_message.lower():
            chat_history.insert(tk.END, "Chatbot: Which city's weather would you like to check?\n")
            if_weather = True
        else:
            # if the user wants to exit
            for exit_command in exit_commands:
                if exit_command in user_message:
                    chat_history.insert(tk.END, "Chatbot: Okay. Bye.\n")
                    user_input.delete(0, tk.END)  
                    chat_history.see(tk.END)
                    background.destroy()
            bot_response = chatbot.generate_response(user_message)
            chat_history.insert(tk.END, "Chatbot: " + bot_response + "\n")  
    
    # Clear the input field
    user_input.delete(0, tk.END)  
    # Scroll to show the latest message
    chat_history.see(tk.END)  

# Bind the Enter key to chat()
user_input.bind("<Return>", chat)

# Send button
send_button = tk.Button(background, text="Send", command=chat) 
send_button.pack(pady=5)  

# Start the chat 
chat_history.insert(tk.END, "Chatbot: Hi, I'm a chatbot. Would you like to chat with me? Try asking me about the weather :)\n\n")

background.mainloop()  
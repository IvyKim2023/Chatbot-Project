## Project Summary
This is a chatbot built using seq2seq model in Tensorflow. (The model is implemented based on Codeacademy's tutorial.) It has an interactive display interface and is able to answer weather-related questions of a specific city accurately.  
The model derived by the current code will be a model trained by 1000 dialogues in daily_dialogues.txt with batch_size = 10 and epochs = 1000. It takes hours to run on a CPU and has limited performance, but is able to handle a conversation that is rather similar to the first 1000 dialogues in daily_dialogues.txt.  
To have better performance, larger data and larger epochs will be needed and the code is better run on a GPU.  
The weather feature is built using OpenWeather API, which can get the current weather of a given city.

---

## Files
**dialogue_pair_up.py:** Split up each line in the cleaned data txt file and pair them up as dialogues  
**preprocessing.py:** Prepare the encoder input, decoder input, and decoder target matrix  
**training_model.py:** Train the model with chosen dimensionality, batch_size, and epochs  
**test_model.py:** Test the model with the generated model trained_model.h5  
**chatbot.py:** Apply this model to a chatbot that can respond with the predicted sequence   
**dispaly.py:** GUI of this chatbot  
**imsdb_sample_movie_scraper:** A sample scraper for movie dialogues. (The code may need a little adjustment to fit the different formats of different movie scripts.)

---

## Data
**friends_dialogues.txt:** Cleaned dialogues from the Friends TV series script. Originally from https://www.kaggle.com/datasets/blessondensil294/friends-tv-series-screenplay-script?resource=download.  
**daily_dialogues.txt:**  Cleaned dialogues from https://www.kaggle.com/datasets/kreeshrajani/3k-conversations-dataset-for-chatbot.






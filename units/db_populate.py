import os
from units.DAO import EmotionColourDAO

def populate_emotioncolour():
    
    # Anger
    EmotionColourDAO.create_emotion(emotion_name="Anger",
                                    black=4.5,
                                    red=8.6,
                                    gray=1.0,
                                    yellow=0,
                                    light_purple=0,
                                    sky_blue=0,
                                    jade=0,
                                    green=0,
                                    aqua=0,
                                    indigo=0.5,
                                    blue=0,
                                    bright_pink=0,
                                    chocolate=0,
                                    dark_yellow=0,
                                    light_green=0,
                                    sample_size=1000)
    
    # Calmness
    EmotionColourDAO.create_emotion(emotion_name="Calmness",
                                    black=0,
                                    red=0,
                                    gray=0,
                                    yellow=0,
                                    light_purple=2.3,
                                    sky_blue=3.1,
                                    jade=0,
                                    green=0,
                                    aqua=1.6,
                                    indigo=0,
                                    blue=2.4,
                                    bright_pink=0,
                                    chocolate=0,
                                    dark_yellow=0,
                                    light_green=0,
                                    sample_size=1000)

    # Contempt
    EmotionColourDAO.create_emotion(emotion_name="Contempt",
                                    black=1.7,
                                    red=0,
                                    gray=1.0,
                                    yellow=0,
                                    light_purple=1.2,
                                    sky_blue=0,
                                    jade=0,
                                    green=0.5,
                                    aqua=0,
                                    indigo=0,
                                    blue=0.5,
                                    bright_pink=0.6,
                                    chocolate=0.7,
                                    dark_yellow=0.8,
                                    light_green=0,
                                    sample_size=1000)
    
    # Disgust
    EmotionColourDAO.create_emotion(emotion_name="Disgust",
                                    black=0,
                                    red=0,
                                    gray=0,
                                    yellow=0,
                                    light_purple=0,
                                    sky_blue=0,
                                    jade=0.5,
                                    green=0.5,
                                    aqua=0,
                                    indigo=0,
                                    blue=0,
                                    bright_pink=0,
                                    chocolate=3.6,
                                    dark_yellow=3.2,
                                    light_green=3.1,
                                    sample_size=1000)

    # Envy
    EmotionColourDAO.create_emotion(emotion_name="Envy",
                                    black=0,
                                    red=1.7,
                                    gray=0,
                                    yellow=0,
                                    light_purple=0,
                                    sky_blue=0,
                                    jade=2.7,
                                    green=3.0,
                                    aqua=0,
                                    indigo=0,
                                    blue=0,
                                    bright_pink=0,
                                    chocolate=0,
                                    dark_yellow=0,
                                    light_green=1.4,
                                    sample_size=1000) 

    # Fear
    EmotionColourDAO.create_emotion(emotion_name="Fear",
                                    black=5.7,
                                    red=2.5,
                                    gray=1.6,
                                    yellow=1.0,
                                    light_purple=0,
                                    sky_blue=0,
                                    jade=0,
                                    green=0,
                                    aqua=0,
                                    indigo=0.9,
                                    blue=0,
                                    bright_pink=0,
                                    chocolate=0,
                                    dark_yellow=0,
                                    light_green=0,
                                    sample_size=1000) 

    # Happiness
    EmotionColourDAO.create_emotion(emotion_name="Happiness",
                                    black=0,
                                    red=0,
                                    gray=0,
                                    yellow=5.3,
                                    light_purple=0,
                                    sky_blue=2.6,
                                    jade=0,
                                    green=0,
                                    aqua=2.3,
                                    indigo=0,
                                    blue=0.6,
                                    bright_pink=1.4,
                                    chocolate=0,
                                    dark_yellow=0,
                                    light_green=0,
                                    sample_size=1000) 
    
    # Jealousy
    EmotionColourDAO.create_emotion(emotion_name="Jealousy",
                                    black=0,
                                    red=2.6,
                                    gray=0,
                                    yellow=0,
                                    light_purple=0,
                                    sky_blue=0,
                                    jade=2.4,
                                    green=2.3,
                                    aqua=0,
                                    indigo=0,
                                    blue=0,
                                    bright_pink=0,
                                    chocolate=0,
                                    dark_yellow=0,
                                    light_green=1.4,
                                    sample_size=1000) 

     # Sadness
    EmotionColourDAO.create_emotion(emotion_name="Sadness",
                                    black=2.4,
                                    red=0,
                                    gray=4.2,
                                    yellow=0,
                                    light_purple=0,
                                    sky_blue=0,
                                    jade=0,
                                    green=0,
                                    aqua=0,
                                    indigo=3.4,
                                    blue=0,
                                    bright_pink=0,
                                    chocolate=0.8,
                                    dark_yellow=0,
                                    light_green=0,
                                    sample_size=1000) 

     # Surprise
    EmotionColourDAO.create_emotion(emotion_name="Surprise",
                                    black=0,
                                    red=0,
                                    gray=0,
                                    yellow=2.6,
                                    light_purple=0.9,
                                    sky_blue=0.6,
                                    jade=0,
                                    green=0,
                                    aqua=2.1,
                                    indigo=0,
                                    blue=0,
                                    bright_pink=2.6,
                                    chocolate=0,
                                    dark_yellow=0,
                                    light_green=0,
                                    sample_size=1000) 
    
    
def check_database_existence(filepath):
                # Check if the file exists
                if os.path.exists(filepath):
                    print(f"The database file '{filepath}' exists.")
                    return True
                else:
                    # Initialize the database
                    print(f"The database file '{filepath}' does not exist.")
                    return False

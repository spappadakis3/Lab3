
import streamlit as st
import requests
import google.generativeai as genai

st.title("Paradise LLM Analysis")


key = st.secrets["key"]
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_episode_data(episode_number):
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    episodes = response.json()
    for episode in episodes:
        if episode["number"] == episode_number:
            return episode
            
    return None

def get_cast_data():
    url = "https://api.tvmaze.com/shows/75030/cast"
    response = requests.get(url)
    return response.json()

all_chars = get_cast_data()
charList = []
for actor in all_chars:
    charList.append(actor["character"]["name"])

def get_all_episodes():
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    return response.json()

all_episodes = get_all_episodes()
episodesList = []
summaryList=[]
for ep in all_episodes:
    episodesList.append(ep["number"])
    summaryList.append(ep["summary"])

def generate_character_info(character_name):
    cast_data = get_cast_data()
    character_info = "Information not found"
    for actor in cast_data:
        if character_name.lower() in actor["character"]["name"].lower():
            character_info = f"Character: {actor['character']['name']}\nActor: {actor['person']['name']}"
            break  
 
    prompt = f"""
    Based on this character information from the TV show "Paradise":
    {character_info}
    
    Please create a detailed profile for this character including:
    1. A brief background story
    2. What is there favorite thing to do in the show
    3. Their main purpose or role in the show
    
    Keep your less than 200 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def predict_next_season(summaryList):
    prompt = f"""
    You are a TV show expert for the show "Paradise" on Hulu. Use the information found in {summaryList} for this prompt.
    
    Based on the typical patterns of TV dramas, predict what might happen in the next season of "Paradise".
    
    Include:
    1. Two possible major storylines
    2. One character who might face a significant challenge
    3. A potential new character or setting
    4. Who may they try to remove from the show in the next season
    
    Keep your less than 300 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
    
def connect_an_episode(episode_number, summaryList):
    prompt = f"""
     You are a TV show expert for the show "Paradise". 
    Based on the episode {episode_number} that the user selcted,  tell the user how this episode builds the overall plot or storyline.
    Make sure to use the summary corresponding to that episode as well {summaryList[episode_number]}
    
    Include:
    1. Three key events from the episode
    2. One character and their role in the episode 
    3. How this helps set the storyline for the remainder of the seaoson
    
    Keep your less than 200 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
    
def compare_characters(char1, char2, summaryList):
 
    prompt = f"""
    Based on the two characters selected {char1} and {char2} 
    and you can use {summaryList} to find more information about the role the characters play in the episodes
    
    Please compare the two characters and include these things:
    1. What strengths do they have in common
    2. What are their roles in the show and how do these differ
    3. Are these characters friends, do they get along, or do they not interact much
    
    Keep your less than 150 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

st.header("Character Information")
character_name = st.text_input("Enter a character name:")
st.write("A few names for example: Gabriela, Xavier, Cal, James . ")
st.write("These are just a few names of the characters in the show in case you do not know any to input")

if st.button("Get Character Info") and character_name:
    with st.spinner("Generating character information..."):
        result = generate_character_info(character_name)
        st.write(result)

st.header("Next Season Predictions")
st.write("Generate a prediction of what might be coming in season 2!")
if st.button("Generate Predictions"):
    with st.spinner("Predicting next season..."):
        predictions = predict_next_season(summaryList)
        st.write(predictions)

st.header("Episode Connections")
st.write("Choose an episode to see how it connects to the overall plot")
episode_number = st.selectbox("Select an Episode Number:", episodesList)
if st.button("Generate Connection"):
    with st.spinner("Determining the connection..."):
        connection = connect_an_episode(episode_number, summaryList)
        st.write(connection)

st.header("Character Comparison")
st.write("Select two characters to see their comparison!")
char1 = st.selectbox("Select your first character:", charList)
char2 = st.selectbox("Select your second character:",charList)
if st.button("Show Comparison"):
    if char1 != char2:
        with st.spinner("Determining the comparison..."):
            compare = compare_characters(char1, char2, summaryList)
            st.write(compare)
    else:
        st.error("Please select two different characters for comparison.")

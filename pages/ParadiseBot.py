
import streamlit as st
import random
import requests
import google.generativeai as genai

st.title("Paradise Chat Bot!")

st.write("Ask me questions about the show Paradise on Hulu!")
st.write("Some question recommendations: ask me about the episodes, cast, and characters!")
api_info = "https://api.tvmaze.com/shows/75030"
cast_api= "https://api.tvmaze.com/shows/75030/cast"
episode_api = "https://api.tvmaze.com/shows/75030/episodes"

def randomEpisode():
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    episodes = response.json()

    episodeList = []
    for ep in episodes:
        episodeList.append(ep['name'])
    return  random.choice(episodeList)

key = st.secrets['key']
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.0-flash')

def episodeNames():
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    episodes = response.json()

    episodeList = []
    for ep in episodes:
        episodeList.append(ep['name'])
    return episodeList

def getEpisodes():
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    episodes = response.json()

    episodeList = []
    for ep in episodes:
        summ = ep['summary']
        summ2 = summ.replace("<p>", "").replace("</p>", "")
        epInfo = f"Episode {ep['number']} from season {ep['season']}: The name is '{ep['name']}', and a quick summary is: {summ2}"
        episodeList.append(epInfo)
    return episodeList

def specificEpisode(episode_number):
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    episodes = response.json()
    for ep in episodes:
        if ep["number"] == episode_number:
            summ = ep['summary']
            summ2 = summ.replace("<p>", "").replace("</p>", "")
            epInfo = f"Episode {ep['number']} from season {ep['season']}: The name is '{ep['name']}', and a quick summary is: {summ2}"
            return epInfo

def getCharacter(name):
    url = f"https://api.tvmaze.com/shows/75030/cast"
    response = requests.get(url)
    cast = response.json()

    for member in cast:
        if member['character']['name'].lower() == name.lower():
            reply = f"{name}'s name in real life is {member['person']['name']}, their birthday is {member['person']['birthday']}"
            return reply
def getAllCharacters():
    url = f"https://api.tvmaze.com/shows/75030/cast"
    response = requests.get(url)
    cast = response.json()
    characters = []
    for member in cast:
        characters.append(f"{member['character']['name']} whose name in real life is {member['person']['name']}, their birthday is {member['person']['birthday']}")

    return characters

if "messages" not in st.session_state:
    st.session_state.messages = []

    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about the show!"):
    
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        if "episode" in prompt.lower():

            if 'favorite' in prompt.lower():
                reply = f"My Favorite Episode is: {randomEpisode()}"
                st.session_state.messages.append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.markdown(reply)
            else:
                
                reply = f"Here is the information of the episode:\n\n"
                api_info = getEpisodes()
                inRange = False
                for i in range(10):
                    if str(i) in prompt:
                        inRange = True
                        api_info = specificEpisode(i)
                        reply = api_info
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                        with st.chat_message("assistant"):
                            st.markdown(reply)
                        
                
                if inRange == False:
                    reply = f"Here are some episodes I found:\n\n"
                
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                        i=1
                        for info in api_info:
                            st.markdown(f"{info.strip()}")
                            i+=1
        
        elif 'character' in prompt.lower():

            url = f"https://api.tvmaze.com/shows/75030/cast"
            response = requests.get(url)
            cast = response.json()
            

            nameGiven = False
            for member in cast:
                if member['character']['name'].lower() in prompt.lower():
                    nameGiven = True
                    reply = f"Here is info on the character: \n"
                    reply = getCharacter(member['character']['name'])
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                        
                
            if nameGiven == False:
                reply = f"Here are some characters I found:\n\n"
                
                st.session_state.messages.append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.markdown(reply)
                    api_info = getAllCharacters()
                    for info in api_info:
                        st.markdown(f"{info.strip()}")
                            

        else:
            convoHistory = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    convoHistory += f"User: {msg['content']}\n"
                else:
                    convoHistory += f"Assistant: {msg['content']}\n"

            convoHistory += f"User: {prompt}\nAssistant:"
            context = ( "The user is asking about the 2025 Hulu series 'Paradise', a political thriller."
                        "The show stars Sterling K. Brown as Secret Service agent Xavier Collins, and has other cast members like James Marsden, Julianne Nicholson, Sarah Shahi, and more." 
                       "Please answer based on this specific TV show."
                       f"You can also use data from these apis {api_info} {cast_api} {episode_api}\n\n" )
            updated_prompt = context + convoHistory
            gemini_response = model.generate_content(updated_prompt)
            reply = gemini_response.text
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)

        
    except:
        st.chat_message("assistant")
        st.error("Error Present")

import streamlit as st
import random
import time
import requests
import google.generativeai as genai


st.write("This is phase 4 chatbot implementation")
st.write("The chatbot can answer questions about what happened in certain episodes or facts about the actors")
st.write("these are just ideas for how we could use it we can do other stuff too")

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
        epInfo = f"Episode {ep["number"]} from season {ep["season"]}: The name is '{ep['name']}', and a quick summary is: {summ2}"
        episodeList.append(epInfo)
    return episodeList

def specificEpisode(episode_number):
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    episodes = response.json()
    st.markdown("is running")
    for ep in episodes:
        if ep["number"] == episode_number:
            summ = ep['summary']
            summ2 = summ.replace("<p>", "").replace("</p>", "")
            epInfo = f"Episode {ep["number"]} from season {ep["season"]}: The name is '{ep['name']}', and a quick summary is: {summ2}"
            return epInfo


        
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
            
            reply = f"Here is the information of the episode:\n\n"
            api_info = getEpisodes()
            inRange = False
            for i in range(10):
                if i in prompt:
                    st.markdown("found episode number")
                    inRange = True
                    api_info = specificEpisode(i)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                        st.markdown(api_info)
                
            if inRange == False:
                reply = f"Here are some episodes I found:\n\n"
                
                st.session_state.messages.append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.markdown(reply)
                    i=1
                    for info in api_info:
                        st.markdown(f"{info.strip()}")
                        i+=1
            
                
                
        else:
            gemini_response = model.generate_content(prompt)
            reply = gemini_response.text
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)

        
    except:
        st.chat_message("assistant")
        st.error("Error Present")


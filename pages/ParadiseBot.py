import streamlit as st
import random
import time
import google.generativeai as genai


st.write("This is phase 4 chatbot implementation")
st.write("The chatbot can answer questions about what happened in certain episodes or facts about the actors")
st.write("these are just ideas for how we could use it we can do other stuff too")

key = st.secrets['key']
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.0-flash')

def getEpisodes():
    url = f"https://api.tvmaze.com/shows/75030/episodes"
    response = requests.get(url)
    episodes = response.json()

    episodeList = []
    for ep in episodes:
        episodeList.append(ep)
    return episodeList

        
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
            api_info = get_show_episodes()
            reply = f"Here are some episodes I found:\n\n{api_info}"
        else:
            gemini_response = model.generate_content(prompt)
            reply = gemini_response.text

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    except:
        st.chat_message("assistant")
        st.error("Error")



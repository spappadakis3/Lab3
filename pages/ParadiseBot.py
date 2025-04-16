import streamlit as st
import random
import time
from openai import OpenAI
from google.generativeai as genai
st.write("This is phase 4 chatbot implementation")
st.write("The chatbot can answer questions about what happened in certain episodes or facts about the actors")
st.write("these are just ideas for how we could use it we can do other stuff too")


def response_generator(prompt):
    #response = random.choice(["Hi there! What can I help you with?","Hi, human! What's up?","Can I help you?"])
    response = prompt
    for word in response.split():
        yield word + " "
        time.sleep(.03)
    return response

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type prompt here"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.write(response_generator(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})




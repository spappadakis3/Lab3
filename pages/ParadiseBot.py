import streamlit as st
st.write("This is phase 4 chatbot implementation")
st.write("The chatbot can answer questions about what happened in certain episodes or facts about the actors")
st.write("these are just ideas for how we could use it we can do other stuff too")

with st.chat_message("user"):
    st.write("Hello! What can I help you with?")

chatPrompt = st.chat_input("Type prompt here")
st.write(chatPrompt)

if chatPrompt == 'Hi':
    st.write("Hi There!")

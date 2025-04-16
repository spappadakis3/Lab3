import streamlit as st
import random
import time
import Paradise_LLM_Analysis



st.write("This is phase 4 chatbot implementation")
st.write("The chatbot can answer questions about what happened in certain episodes or facts about the actors")
st.write("these are just ideas for how we could use it we can do other stuff too")

key = st.secrets['key']


def response_generator(prompt):
    #response = random.choice(["Hello there! How can I assist you today?","Hi, human! Is there anything I can help you with?","Do you need help?"])
    response = prompt
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
        
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What can I help you with?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

     if key:
          llm_response = Paradise_LLM_Analysis.generate_llm_response(prompt, key)
          st.session_state.messages.append({"role": "assistant", "content": llm_response})
          with st.chat_message("assistant"):
            st.markdown(llm_response)

        
    st.session_state.messages.append({"role": "assistant", "content": response})


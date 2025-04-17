
import streamlit as st

# Title of App
st.title("Web Development Lab03")
st.image("images/paradise_image.jpg", width=300)

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 1, Web Development - Section A")
st.subheader("Sophia Pappadakis, Lilli Mahlke")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. Paradise Show Info! This page features a line graph of episode ratings, with options to view an image and summary for each episode. It also displays an image of a selected actor and lets users compare episode lengths via an interactive bar graph. 
2. Paradise LLM Analysis - This page allows you to interact with a chatbot to ask questions about next season predictions, character analysis, and epsiode connections to the overall plot of the show!
3. ParadiseBot- Interact with a chatbot and ask questions about the show Paradise!

""")

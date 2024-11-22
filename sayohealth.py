#import all necessary libraries
import os, json
import streamlit as st
from groq import Groq
from PIL import Image
#from dotenv import load_dotenv


#create the streamlit configuration page
st.set_page_config(page_title="SAYO HEALTH", layout= "centered", page_icon="👪")


api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

#initialize the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

#create title ans the first markdown
st.title("SAYO HEALTH BOT")
st.markdown(
    """
    It is vital to understand that good health is good wealth.....
    I AM HERE TO HELP YOU ACHIEVE GOOD HEALTH
    """
)
#load a display image
image1= Image.open("image5.png")
st.image(image1, use_column_width=True, width=350)

#display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
#user input
user_prompt= st.chat_input("ask sayo...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Send user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are SayoMetrics, a friendly and helpful AI assistant. When asked about your name, identify yourself as SayoMetrics AI. Your creatorr is Benjamin Uka, a researcher and developer at Benjitable DS, a company that focuses on developing and applying various forms of artificial intelligence to help humans communicate more effectively, you will only answer health related question"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

#add a sidebar with contact details and chatbot image
st.sidebar.title("About SAYO Ai")
image2 = Image.open("simsage1.png")
st.sidebar.image(image2, caption="benGPT", use_column_width=True)
st.sidebar.markdown(
    """
    SAYO Health is a powerful AI assistant designed to learn and assist you with various tasks. 

    **Contact us:**
    * Email: sayohealth@gmail.com
    * Phone: +2348139656309
    """
)

st.sidebar.button("Learn More")

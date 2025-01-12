import os
import streamlit as st 
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm  = ChatGroq(model="mixtral-8x7b-32768", temperature=0.2)
fruit=st.text_input("enter the fruit name")
if fruit:
    result = llm.invoke(f"You are an experienced comedian. You will be given a fruit, on which you have to make a joke.\n\nFruit: {fruit}").content
    st.write(result)
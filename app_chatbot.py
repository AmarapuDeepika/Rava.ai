import os
import streamlit as st 
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm  = ChatGroq(model="llama3-8b-8192", temperature=0.2)
#fruit=st.text_input("enter the fruit name")
#if fruit:
result = llm.invoke(f"You are the owner of a famous cloths store.You need to answer the queries of the customers who are visited your shop.").content
st.write(result)
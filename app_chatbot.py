import os
import streamlit as st 
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm  = ChatGroq(model="llama3-8b-8192", temperature=0.2)
st.title("Welcom to Cloth Store Bot")
query = st.text_input("Ask any question you want to know about our store!")
irrelavent_query="Sorry sir/madam I don't have information regarding that.\
     I am here to answer your queries regarding our cloth store"
if query:
    result = llm.invoke(f"You are the owner of a famous cloth store in India named,\
    FS cloth store.Your role is to answer the customer queries about the store in a simple \
    and polite way.Ensure your responses are clear and have to follow a specific format\
    and also include emojis for the better user experience.If a query is unrelated \
    to clothing store,respond with '{irrelavent_query}'.\n\n query:{query}.").content
    st.write(result)


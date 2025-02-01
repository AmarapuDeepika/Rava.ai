import requests
from bs4 import BeautifulSoup
import os
import streamlit as st 
from langchain_groq import ChatGroq
import time

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm  = ChatGroq(model="llama3-8b-8192", temperature=0.2)

st.title("Welcome to the content generator based on URL")

url = st.text_input("Enter the URL on which you want to ask questions", key="url_input")
irrelavent_query = "Sorry, the URL you provided doesn't have this information."

def func_content(url):
    try:
        start_time = time.time() 
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

            #links=[a["href"] for a in soup.find_all('a',href=True)]

            content = "\n".join(headings + paragraphs)
            end_time = time.time() 
            scraping_time = end_time - start_time
            if content.strip():
                return content, "Scrapped successfully",scraping_time
            else:
                return None, "No meaningful content found on the webpage",scraping_time
        else:
            return None, f"Request failed with status code: {response.status_code}",0
    except Exception as e:
        return None, f"An error occurred: {str(e)}",0

if url:
    content, status_msg,scraping_time = func_content(url)
    #st.write(status_msg)
    if not content:
        st.error(status_msg)
    if content:
        st.success(status_msg)
        #st.write(content)
        st.text(f"Time taken for web scraping: {scraping_time:.2f} seconds")
        query = st.text_input("Ask the question related to the URL")  
        if query:
            llm_strat_time=time.time()
            result = llm.invoke(
                f"You are the virtual assistant.\
                Your role is to respond to the user queries \
                only from the content scraped from the URL :'{content}'in a clear and concise manner.\
                You must not allowed to give the response from any other resources apart from\
                this content:{content}.If the user query is not related to the \
                scraped content,then you need to respond only like: \
                '{irrelavent_query}'.\n\nQuery: {query}"
            ).content
            llm_end_time=time.time()
            llm_time = llm_end_time-llm_strat_time
            st.write(result)
            st.write(f"Time taken for LLM response: {llm_time:.2f} seconds")
            st.write(f"Total time taken: {scraping_time + llm_time:.2f} seconds")
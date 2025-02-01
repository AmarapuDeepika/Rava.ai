import requests
from bs4 import BeautifulSoup
import os
import streamlit as st
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer, util
import time
import json

# Initialize constants and models
URL_HISTORY_FILE = "url_history.json"
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)
model = SentenceTransformer('all-MiniLM-L6-v2')

st.title("Welcome to the Content Generator Based on URL")
irrelavent_query = "Sorry, the URL you provided doesn't have this information."

# Load previous URLs and content
def load_url_history():
    if os.path.exists(URL_HISTORY_FILE):
        with open(URL_HISTORY_FILE, 'r') as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):  
                    return data
                else:
                    return {}  
            except json.JSONDecodeError:
                return {} 
    return {}

# Save URL history and cached content to file
def save_url_history(url_history):
    with open(URL_HISTORY_FILE, 'w') as file:
        json.dump(url_history, file)

# Ensure url_cache is a dictionary
url_cache = load_url_history()
if not isinstance(url_cache, dict): 
    url_cache = {}

def chunk_content(content, max_chunk_size=3000):
    chunks = []
    while len(content) > max_chunk_size:
        split_index = content[:max_chunk_size].rfind(".")
        if split_index == -1:
            split_index = max_chunk_size
        chunks.append(content[:split_index + 1].strip())
        content = content[split_index + 1:].strip()
    chunks.append(content)
    return chunks

def func_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
            content = "\n".join(headings + paragraphs)
            if content.strip():
                return content, "URL scraped successfully"
            else:
                return None, "No meaningful content found on the webpage"
        else:
            return None, f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def get_most_relevant_chunk(query, chunks):
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, chunk_embeddings)[0]
    best_match_idx = similarities.argmax().item()
    return chunks[best_match_idx]

# State to track whether scraping has just been done
scraping_done = False
current_url = ""

url = st.text_input("Enter the URL on which you want to ask questions", key="url_input")

# Using session state to track the scraping message
if 'scraping_msg' not in st.session_state:
    st.session_state.scraping_msg = None
if 'scrape_time' not in st.session_state:
    st.session_state.scrape_time = 0
if 'scraping_done' not in st.session_state:
    st.session_state.scraping_done = False

if url:
    if url not in url_cache: 
        scrape_start_time = time.time()
        content, status_msg = func_content(url)
        scrape_time = time.time() - scrape_start_time
        if content:
            url_cache[url] = content  
            save_url_history(url_cache)
           
            st.session_state.scraping_msg = f"URL successfully scraped: {scrape_time:.2f} seconds"
            st.session_state.scrape_time = scrape_time
            st.session_state.scraping_done = True  
        else:
            st.error(status_msg)
            content = None
    else:  
        content = url_cache[url]
        scrape_time = 0  
        if not st.session_state.scraping_msg or current_url != url:
            st.session_state.scraping_msg = "URL already scraped. No scraping required!"
        st.session_state.scrape_time = 0
        st.session_state.scraping_done = True

    # Display the scraping message
    if st.session_state.scraping_done and "successfully scraped" in st.session_state.scraping_msg:
        st.success(st.session_state.scraping_msg)
    else:
        st.info(st.session_state.scraping_msg)

    current_url = url


    if content:  
        query = st.text_input("Ask a question related to the URL", key="query_input")
        submit_query = st.button("Submit Query")

        if submit_query:
            if query.strip():
                #chunk time
                chunks_start_time = time.time()
                chunks = chunk_content(content, max_chunk_size=3000)
                relevant_chunk = get_most_relevant_chunk(query, chunks)
                chunks_time = time.time() - chunks_start_time

                # LLM response
                llm_start_time = time.time()
                if relevant_chunk:
                    result = llm.invoke(
                        f"You are a highly organized virtual assistant. Provide a concise and well-structured response "
                        f"to the user query using only the provided content chunk: '{relevant_chunk}'. "
                        f"You must not give the response from any other resources apart from this content: {relevant_chunk}. "
                        f"If the user query is not related to the content provided, respond only with: '{irrelavent_query}'.\n\nQuery: {query}"
                    ).content
                    st.write(result)
                else:
                    st.write(irrelavent_query)
                llm_time = time.time() - llm_start_time

                # Calculate total time
                total_time = (
                    st.session_state.scrape_time + chunks_time + llm_time
                    if st.session_state.scraping_done
                    else chunks_time + llm_time
                )

                # Display timings
                if st.session_state.scraping_done:
                    st.write(f"Scraping time: {st.session_state.scrape_time:.2f} seconds")
                st.write(f"Chunk processing time: {chunks_time:.2f} seconds")
                st.write(f"LLM response time: {llm_time:.2f} seconds")
                st.success(f"Total time: {total_time:.2f} seconds")
            else:
                st.error("Please enter a query to get a response.")
                
# Display URL history
# if st.button("Show Cached URLs"):
#     if url_cache:
#         st.write("### Cached URLs:")
#         for cached_url in url_cache.keys():
#             st.write(f"- {cached_url}")
#     else:
#         st.write("No URLs are currently cached.")


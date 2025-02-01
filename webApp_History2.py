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
            paragraphs = soup.find_all(["p", "ul", "li", "ol"])
            content = " ".join([tag.get_text() for tag in paragraphs])
            if content:
                return content, "URL scraped successfully"
            else:
                return None, "No meaningful content found on the webpage"
        else:
            return None, f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def get_most_relevant_chunks(query, chunks, top_n):
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, chunk_embeddings)[0]
    # best_match_idx = similarities.argmax().item()
    # return chunks[best_match_idx]
    top_indices = similarities.topk(top_n).indices
    return [chunks[i] for i in top_indices]

# State to track whether scraping has just been done

url = st.text_input("Enter the URL on which you want to ask questions", key="url_input")

# Initialize session state variables
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""
if 'scraping_msg' not in st.session_state:
    st.session_state.scraping_msg = None
if 'scrape_time' not in st.session_state:
    st.session_state.scrape_time = 0
if 'scraping_done' not in st.session_state:
    st.session_state.scraping_done = False
if 'is_new_scraping' not in st.session_state:
    st.session_state.is_new_scraping = False

# Check if the URL has changed
if url and url != st.session_state.current_url:
    st.session_state.current_url = url  # Update the current URL in session state
    st.session_state.scraping_msg = None
    st.session_state.scrape_time = 0
    st.session_state.scraping_done = False
    st.session_state.is_new_scraping = False  # Reset the new scraping flag

if url:
    if url not in url_cache:  # New URL, perform scraping
        scrape_start_time = time.time()
        content, status_msg = func_content(url)
        scrape_time = time.time() - scrape_start_time

        if content:
            url_cache[url] = content  # Cache the scraped content
            save_url_history(url_cache)

            st.session_state.scraping_msg = f"URL successfully scraped: {scrape_time:.2f} seconds."
            st.session_state.scrape_time = scrape_time
            st.session_state.scraping_done = True
            st.session_state.is_new_scraping = True  # Mark as new scraping
        else:
            st.error(status_msg)
            content = None
    else:  # URL is already cached
        content = url_cache[url]
        if not st.session_state.is_new_scraping:
            st.session_state.scraping_msg = "URL already scraped. No scraping required!"
            st.session_state.scrape_time = 0
        st.session_state.scraping_done = True

    # Display the scraping message
    if st.session_state.scraping_msg:
        if st.session_state.is_new_scraping:
            st.success(st.session_state.scraping_msg)
        else:
            st.info(st.session_state.scraping_msg)

    # if st.session_state.scraping_msg:
    #     st.success(st.session_state.scraping_msg)

    # Handle query submission
    if content:
        query = st.text_input("Ask a question related to the URL", key="query_input")
        submit_query = st.button("Submit Query")

        if submit_query:
            if query.strip():
                # Process chunks and query
                chunks_start_time = time.time()
                chunks = chunk_content(content, max_chunk_size=3000)
                top_chunks = get_most_relevant_chunks(query, chunks, top_n=3)
                combined_content = " ".join(top_chunks)
                #st.write(combined_content)
                chunks_time = time.time() - chunks_start_time

                # LLM response
                llm_start_time = time.time()
                if combined_content:
                    result = llm.invoke(
                        f"You are a highly organized virtual assistant. Provide a clear, detailed and well-structured response "
                        f"to the user query using only the provided content chunks: '{combined_content}'. "
                        f"You must not give the response from any other resources apart from this content: {combined_content}. "
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
                if st.session_state.scraping_done and st.session_state.is_new_scraping:
                    st.write(f"Scraping time: {st.session_state.scrape_time:.2f} seconds")
                st.write(f"Chunk processing time: {chunks_time:.2f} seconds")
                st.write(f"LLM response time: {llm_time:.2f} seconds")
                st.success(f"Total time: {total_time:.2f} seconds")
            else:
                st.error("Please enter a query to get a response.")
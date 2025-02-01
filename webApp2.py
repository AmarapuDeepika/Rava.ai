import requests
from bs4 import BeautifulSoup
import os
import streamlit as st 
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer, util
import time

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm  = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

st.title("Welcome to the content generator based on URL")

url = st.text_input("Enter the URL on which you want to ask questions", key="url_input")
irrelavent_query = "Sorry, the URL you provided doesn't have this information."

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_content(content, max_chunk_size=3000):
    """Split content into chunks of a specified maximum size."""
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

            #links=[a["href"] for a in soup.find_all('a',href=True)]
            content = "\n".join(headings + paragraphs)
            if content.strip():
                return content, "URL scrapped successfully"
            else:
                return None, "No meaningful content found on the webpage"
        else:
            return None, f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def get_most_relevant_chunk(query, chunks):
    """Find the single most relevant chunk using semantic similarity."""
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, chunk_embeddings)[0]
    best_match_idx = similarities.argmax().item()

    return chunks[best_match_idx]

if url:
    total_start_time = time.time()

    scrape_start_time = time.time()
    content, status_msg = func_content(url)
    scrape_time = time.time()-scrape_start_time
    
    if content:
        st.success(status_msg)
        st.write(f"Scraping time: {scrape_time:.2f} seconds")

        query = st.text_input("Ask the question related to the URL", key="query_input") 
        submit_query = st.button("Submit Query")
        if submit_query:  # This ensures handling even if no query is entered yet
            if query.strip(): 
                chunks_start_time = time.time()

                chunks = chunk_content(content, max_chunk_size=3000)
                relevant_chunk = get_most_relevant_chunk(query, chunks)

                chunks_end_time = time.time()-chunks_start_time
                st.write(f"chunks time: {chunks_end_time:.2f} seconds")

                llm_start_time=time.time()
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
                llm_time= time.time()-llm_start_time
                st.write(f"LLM response time : {llm_time:.2f} seconds")

                total_time = time.time()-total_start_time
                st.success(f"Total time: {total_time:.2f} seconds")
            else:
                st.info("please enter a query to get response")
        
    else:
        st.error(status_msg)

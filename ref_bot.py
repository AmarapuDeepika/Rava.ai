import os
import time
import numpy as np
from bs4 import BeautifulSoup
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import streamlit as st
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.1)

# Load embedding model
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

embedding_model = load_embedding_model()

# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all(["p", "ul", "li"])
            content = " ".join([tag.get_text() for tag in paragraphs])
            return content
        else:
            st.error("Failed to fetch website content. Please check the URL.")
            return None
    except Exception as e:
        st.error(f"An error occurred while scraping: {e}")
        return None

# Function to split text into chunks
def split_text_into_chunks(text, max_length=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += len(word) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

# Function to calculate embeddings
@st.cache_data
def calculate_embeddings(chunks):
    return embedding_model.encode(chunks, convert_to_tensor=True)

# Function to perform semantic search
def perform_semantic_search(query, chunks, chunk_embeddings, top_n=2):
    # Generate embedding for the user query
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)
    # Compute similarity between query embedding and chunk embeddings
    similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]
    # Get indices of top N similar chunks
    top_indices = np.argsort(similarities)[::-1][:top_n]
    # Retrieve the corresponding chunks and their similarity scores
    top_chunks = [(chunks[i], similarities[i]) for i in top_indices]
    return top_chunks

# Streamlit app title
st.title("Enhanced Website-Based Chatbot")

# Input for website URL
url = st.text_input("Enter the website URL to scrape:")

if st.button("Scrape Website"):
    content = scrape_website(url)
    if content:
        st.session_state["scraped_content"] = content
        chunks = split_text_into_chunks(content)
        chunk_embeddings = calculate_embeddings(chunks)
        st.session_state["chunks"] = chunks
        st.session_state["chunk_embeddings"] = chunk_embeddings
        st.success("Website content scraped successfully!")
    else:
        st.error("Failed to scrape website content.")

# Ensure session state variables are initialized
if "scraped_content" not in st.session_state:
    st.session_state["scraped_content"] = ""

if "chunks" not in st.session_state:
    st.session_state["chunks"] = []

if "chunk_embeddings" not in st.session_state:
    st.session_state["chunk_embeddings"] = []

user_input = st.text_input("Enter your question:")

if st.button("Get Response"):
    if not st.session_state["scraped_content"]:
        st.error("Please scrape a website first!")
    else:
        start_time = time.time()  # Start timer

        # Perform semantic search
        query = user_input
        top_chunks = perform_semantic_search(
            query, st.session_state["chunks"], st.session_state["chunk_embeddings"], top_n=2
        )
        combined_context = "\n\n".join([chunk for chunk, _ in top_chunks])

        # Generate response using the Groq LLM
        prompt = (f"You are a content-based chatbot. Give the query related information particularly and as whatever is present there. "
                  f"The following are relevant sections from the website content:\n\n"
                  f"{combined_context}\n\n"
                  f"Answer the question as comprehensively as possible based strictly on the above content. "
                  f"Otherwise, don't manipulate or divert the answer for the question with provided content. "
                  f"If the question is unrelated, respond with: "
                  f"'Sorry, the requested information is not available in the website content.'\n\n"
                  f"Question: {query}")
        response = llm.invoke(prompt).content

        end_time = time.time()  # End timer
        latency = end_time - start_time
        st.success(f"Response generated in {latency:.2f} seconds!")

        st.write(f"*Response:* {response}")
        st.write(f"*Response Time:* {latency:.2f} seconds")
        st.markdown("---")
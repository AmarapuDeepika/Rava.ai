import streamlit as st
from bs4 import BeautifulSoup
import requests
import os
from langchain_groq import ChatGroq
from uuid import uuid4
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm  = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

# Function to scrape content from a URL
def scrape_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = []

            # Extract headings, paragraphs, and list items
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            paragraphs = soup.find_all('p')
            lists = soup.find_all(['ul', 'ol'])

            content.extend([heading.get_text(strip=True) for heading in headings])
            content.extend([para.get_text(strip=True) for para in paragraphs])
            for list_tag in lists:
                content.extend([li.get_text(strip=True) for li in list_tag.find_all('li')])

            if content:
                return ''.join(content), "URL scraped successfully"
            else:
                return None, "No meaningful content found on the webpage"
        else:
            return None, f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"


# Function to create a vector store
def create_vector_store(content, url):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=300
        )
    chunks = text_splitter.split_text(content)
    documents = [Document(page_content=chunk, metadata={"source": url}) for chunk in chunks]
    vector_store = FAISS.from_documents(documents, embedding_model)
    return vector_store

# Function to query the vector store
def query_vector_store(vector_store, query):
    response = vector_store.similarity_search_with_score(query, k=5)
    return response

# Streamlit UI
st.title("Web Content Scraper and Query Tool")

# URL Input
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

url = st.text_input("Enter a URL to scrape:", placeholder="https://example.com")
irrelavent_query = "Sorry, the URL you provided doesn't have this information."
if url:
    with st.spinner("Scraping the URL..."):
        content, msg = scrape_content(url)
        st.write(msg)

    if content:
        with st.spinner("Creating the vector store..."):
            st.session_state.vector_store = create_vector_store(content, url)
        st.success("Vector store created successfully!")
    else:
        st.error("Scraping failed. Please enter a valid URL.")

# Query Input
if st.session_state.vector_store:
    query = st.text_input("Enter your query to search the scraped content:")
    if query:
        with st.spinner("Searching the vector store..."):
            results = query_vector_store(st.session_state.vector_store, query)

        # st.write("### Query Results:")
        # for i, (doc, score) in enumerate(results):
        #     st.write(f"**Result {i + 1}:** {doc.page_content}")
        #     st.write(f"_Relevance Score:_ {score:.2f}")

             # Extract the top document content and their sources
            top_chunks = [doc.page_content for doc, _ in results]
            sources = {doc.metadata["source"] for doc, _ in results}  # Use a set to get distinct sources
            combined_content = " ".join(top_chunks)  # Combine all top chunks into a single string
            print(combined_content)
            if combined_content:
                result = llm.invoke(
                    f"You are a highly organized virtual assistant. Provide a clear, detailed and well-structured response "
                    f"to the user query using only the provided content chunks: '{combined_content}'. "
                    f"You must not give the response from any other resources apart from this content: {combined_content}. "
                    f"If the user query is not related to the content provided, respond only with: '{irrelavent_query}'.\n\nQuery: {query}"
                ).content
                st.write("### Response:")
                st.write(result)

                # Determine and display the source(s)
                st.write("### Source(s):")
                if len(sources) == 1:
                    st.write(next(iter(sources)))  # Display the single source
                else:
                    for source in sources:
                        st.write(source)  # Display each distinct source
            else:
                st.write("No relevant content found to answer your query.")
    else:
        st.error("Enter a valid query!")

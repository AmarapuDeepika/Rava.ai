import os
import streamlit as st 
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm  = ChatGroq(model="llama3-8b-8192", temperature=0.2)
st.title("Welcom to FS Cloth Store Bot")
query = st.text_input("Ask any question you want to know about our store!")
irrelavent_query="Sorry sir/madam I don't have information regarding that.\
     I am here to answer your queries regarding our cloth store"

#cloths data
clothing_data = [
    {"Type": "Shirt", "Gender": "Men", "Price": 1299, "Brand": "Levi's", "Color": "Blue", "Discount": "10%", "Rating": 4.2, "Delivery Time": "2 days", "Size": "M", "Occasion": "Casual", "Shape": "Slim Fit"},
    {"Type": "T-shirt", "Gender": "Women", "Price": 1199, "Brand": "Nike", "Color": "Black", "Discount": "5%", "Rating": 4.5, "Delivery Time": "3 days", "Size": "S", "Occasion": "Sports", "Shape": "Regular"},
    {"Type": "Jeans", "Gender": "Men", "Price": 2499, "Brand": "Wrangler", "Color": "Blue", "Discount": "20%", "Rating": 4.0, "Delivery Time": "4 days", "Size": "L", "Occasion": "Casual", "Shape": "Straight"},
    {"Type": "Jacket", "Gender": "Men", "Price": 3299, "Brand": "Adidas", "Color": "Grey", "Discount": "15%", "Rating": 4.8, "Delivery Time": "1 day", "Size": "L", "Occasion": "Winter", "Shape": "Regular"},
    {"Type": "Dress", "Gender": "Women", "Price": 2999, "Brand": "Zara", "Color": "Red", "Discount": "0%", "Rating": 4.3, "Delivery Time": "5 days", "Size": "M", "Occasion": "Formal", "Shape": "A-line"},
    {"Type": "Shorts", "Gender": "Men", "Price": 1499, "Brand": "Puma", "Color": "Black", "Discount": "10%", "Rating": 3.9, "Delivery Time": "3 days", "Size": "M", "Occasion": "Casual", "Shape": "Slim Fit"},
    {"Type": "Sweater", "Gender": "Women", "Price": 1999, "Brand": "H&M", "Color": "Pink", "Discount": "25%", "Rating": 4.6, "Delivery Time": "2 days", "Size": "L", "Occasion": "Winter", "Shape": "Regular"},
    {"Type": "Skirt", "Gender": "Women", "Price": 1699, "Brand": "Mango", "Color": "Blue", "Discount": "5%", "Rating": 4.1, "Delivery Time": "3 days", "Size": "S", "Occasion": "Casual", "Shape": "Flared"},
    {"Type": "Blouse", "Gender": "Women", "Price": 1799, "Brand": "Uniqlo", "Color": "Green", "Discount": "10%", "Rating": 4.2, "Delivery Time": "4 days", "Size": "M", "Occasion": "Formal", "Shape": "Regular"},
    {"Type": "Hoodie", "Gender": "Men", "Price": 2499, "Brand": "Nike", "Color": "Red", "Discount": "20%", "Rating": 4.4, "Delivery Time": "1 day", "Size": "XL", "Occasion": "Sports", "Shape": "Regular"}
]

if query:
    result = llm.invoke(f"You are the owner of a famous cloth store in India named,\
    FS cloth store.Your store has the different cloths and corresponding details mentioned in {clothing_data}.\
    Your role is to answer the customer queries about the store in a simple \
    and polite way.Ensure your responses are clear and based on the clothing_data only and have to follow a specific format\
    and also include emojis for the better user experience.If a query is unrelated \
    to clothing store,respond with '{irrelavent_query}'.If the user asks for items that\
    are not there in your store ,then you have to reply them as 'sorry sir/mam we \
    don't have those items.\n\n query:{query}.").content
    st.write(result)


import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load semantic search model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Clothing data with prices in rupees
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

# Convert clothing data to DataFrame
clothing_df = pd.DataFrame(clothing_data)

# Streamlit interface
st.title("Clothing Store Bot")

# Knowledge base for queries
knowledge_base = {
    "brands": "We have {num_brands} unique brands available.",
    "types": "We offer the following types of clothing: {types}.",
    "average price": "The average price of our clothing is ₹{avg_price:.2f}.",
    "highest rated": "The highest-rated item is a {type} from {brand} with a rating of {rating}.",
    "discounts": "{num_discounts} items currently have discounts.",
    "colors": "We offer clothing in the following colors: {colors}.",
    "sizes": "Available sizes are: {sizes}.",
    "fastest delivery": "The fastest delivery time is {delivery_time} for {type} from {brand}.",
    "best deal": "The highest discount is {discount} on {type} from {brand}.",
    "price range": "Our prices range from ₹{min_price:.2f} to ₹{max_price:.2f}."
}

# Define queries related to clothing
clothing_related_queries = [
    "brands", "types", "average price", "highest rated", "discounts", "colors", "sizes", 
    "fastest delivery", "best deal", "price range"
]

# Encode queries for semantic matching
encoded_knowledge = model.encode(list(knowledge_base.keys()), convert_to_tensor=True)

# User query input
user_query = st.text_input("Ask me anything about our clothing store:")

# Process query and respond
if user_query:
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, encoded_knowledge)[0]
    best_match_idx = similarities.argmax().item()
    best_match_key = list(knowledge_base.keys())[best_match_idx]

    # Check if the query is related to clothing
    if best_match_key in clothing_related_queries:
        # Respond with the appropriate clothing-related information
        if best_match_key == "brands":
            num_brands = clothing_df['Brand'].nunique()
            st.write(knowledge_base[best_match_key].format(num_brands=num_brands))

        elif best_match_key == "types":
            unique_types = ', '.join(clothing_df['Type'].unique())
            st.write(knowledge_base[best_match_key].format(types=unique_types))

        elif best_match_key == "average price":
            avg_price = clothing_df['Price'].mean()
            st.write(knowledge_base[best_match_key].format(avg_price=avg_price))

        elif best_match_key == "highest rated":
            highest_rated = clothing_df.loc[clothing_df['Rating'].idxmax()]
            st.write(knowledge_base[best_match_key].format(
                type=highest_rated['Type'],
                brand=highest_rated['Brand'],
                rating=highest_rated['Rating']
            ))

        elif best_match_key == "discounts":
            discounts = clothing_df[clothing_df['Discount'] != '0%']
            st.write(knowledge_base[best_match_key].format(num_discounts=len(discounts)))

        elif best_match_key == "colors":
            unique_colors = ', '.join(clothing_df['Color'].unique())
            st.write(knowledge_base[best_match_key].format(colors=unique_colors))

        elif best_match_key == "sizes":
            unique_sizes = ', '.join(clothing_df['Size'].unique())
            st.write(knowledge_base[best_match_key].format(sizes=unique_sizes))

        elif best_match_key == "fastest delivery":
            fastest_delivery = clothing_df.loc[clothing_df['Delivery Time'].idxmin()]
            st.write(knowledge_base[best_match_key].format(
                delivery_time=fastest_delivery['Delivery Time'],
                type=fastest_delivery['Type'],
                brand=fastest_delivery['Brand']
            ))

        elif best_match_key == "best deal":
            best_deal = clothing_df.loc[clothing_df['Discount'].str.rstrip('%').astype(int).idxmax()]
            st.write(knowledge_base[best_match_key].format(
                discount=best_deal['Discount'],
                type=best_deal['Type'],
                brand=best_deal['Brand']
            ))

        elif best_match_key == "price range":
            min_price = clothing_df['Price'].min()
            max_price = clothing_df['Price'].max()
            st.write(knowledge_base[best_match_key].format(min_price=min_price, max_price=max_price))
    else:
        # Respond with a generic "Sorry, I don't have that information" for unrelated queries
        st.write("Sorry, I don't have that information")

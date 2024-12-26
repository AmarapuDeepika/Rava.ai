# import streamlit as st
# import pandas as pd
# from sentence_transformers import SentenceTransformer, util
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# # Load semantic search model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Predefined data
# types = ['Shirt', 'T-shirt', 'Jeans', 'Jacket', 'Dress', 'Shorts', 'Sweater', 'Skirt', 'Blouse', 'Hoodie']
# brands = ['Zara', 'Nike', 'Biba', 'Adidas', 'H&M', 'Levi\'s', 'Forever 21', 'Raymond', 'FabIndia', 'Puma']
# colors = ['Blue', 'Black', 'Blue', 'Grey', 'Red', 'Black', 'Pink', 'Blue', 'Green', 'Red']
# prices = [1299, 1199, 2499, 3299, 2999, 1499, 1999, 1699, 1799, 2499]
# discounts = ['10%', '5%', '20%', '15%', '0%', '10%', '25%', '5%', '10%', '20%']
# ratings = [4.2, 4.5, 4.0, 4.8, 4.3, 3.9, 4.6, 4.1, 4.2, 4.4]
# delivery_times = ['2 days', '3 days', '4 days', '1 day', '5 days', '3 days', '2 days', '3 days', '4 days', '1 day']
# shapes = ['Slim Fit', 'Regular', 'Straight', 'Regular', 'A-line', 'Slim Fit', 'Regular', 'Flared', 'Regular', 'Regular']
# occasions = ['Casual', 'Sports', 'Casual', 'Winter', 'Formal', 'Casual', 'Winter', 'Casual', 'Formal', 'Sports']
# sizes = ['M', 'S', 'L', 'L', 'M', 'M', 'L', 'S', 'M', 'XL']

# # Combine into a DataFrame
# clothing_data = pd.DataFrame({
#     'Type': types,
#     'Brand': brands,
#     'Color': colors,
#     'Price': prices,
#     'Discount': discounts,
#     'Rating': ratings,
#     'Delivery Time': delivery_times,
#     'Shape': shapes,
#     'Occasion': occasions,
#     'Size': sizes
# })

# # Streamlit interface
# st.title("Clothing Store Bot")

# # Knowledge base for queries
# knowledge_base = {
#     "brands": "We have {num_brands} unique brands available, those are : <br>{brands}",
#     "types": "We offer the following types of clothing: {types}.",
#     "average price": "The average price of our clothing is ₹{avg_price:.2f}.",
#     "highest rated": "The highest-rated item is a {type} from {brand} with a rating of {rating}.",
#     "discounts": "{num_discounts} items currently have discounts.",
#     "colors": "We offer clothing in the following colors: {colors}.",
#     "sizes": "Available sizes are: {sizes}.",
#     "fastest delivery": "The fastest delivery time is {delivery_time} for {type} from {brand}.",
#     "best deal": "The highest discount is {discount} on {type} from {brand}.",
#     "price range": "Our prices range from ₹{min_price:.2f} to ₹{max_price:.2f}."
# }

# # Encode queries for semantic matching
# encoded_knowledge = model.encode(list(knowledge_base.keys()), convert_to_tensor=True)

# # TF-IDF Vectorizer for keyword search
# tfidf_vectorizer = TfidfVectorizer()
# tfidf_matrix = tfidf_vectorizer.fit_transform(list(knowledge_base.keys()))

# SIMILARITY_THRESHOLD = 0.35  # Minimum similarity to trigger response

# # Hybrid search combining semantic and keyword matching
# def hybrid_search(query):
#     # Encode with SentenceTransformer
#     query_embedding = model.encode(query, convert_to_tensor=True)
#     semantic_similarities = util.pytorch_cos_sim(query_embedding, encoded_knowledge)[0]

#     # TF-IDF for keyword matching
#     tfidf_query_vector = tfidf_vectorizer.transform([query])
#     keyword_similarities = np.dot(tfidf_query_vector, tfidf_matrix.T).toarray()[0]

#     # Combine scores (weighted average)
#     combined_scores = 0.7 * semantic_similarities.cpu().numpy() + 0.3 * keyword_similarities
#     best_match_idx = np.argmax(combined_scores)
#     best_match_score = combined_scores[best_match_idx]

#     return best_match_idx, best_match_score

# # User query input
# user_query = st.text_input("Ask me anything about our clothing store:")

# # Process query and respond
# if user_query:
#     best_match_idx, best_match_score = hybrid_search(user_query)
#     best_match_key = list(knowledge_base.keys())[best_match_idx]

#     if best_match_score < SIMILARITY_THRESHOLD:
#         st.write("Sorry... I'm here to help with clothing-related questions.")
#     else:
#         if best_match_key == "brands":
#             num_brands = clothing_data['Brand'].nunique()
#             brandS = ', '.join(clothing_data['Brand'].unique())
#             st.markdown(knowledge_base[best_match_key].format(num_brands=num_brands, brands=brandS), unsafe_allow_html=True)
#         elif best_match_key == "types":
#             unique_types = ', '.join(clothing_data['Type'].unique())
#             st.write(knowledge_base[best_match_key].format(types=unique_types))

#         elif best_match_key == "average price":
#             avg_price = clothing_data['Price'].mean()
#             st.write(knowledge_base[best_match_key].format(avg_price=avg_price))

#         elif best_match_key == "highest rated":
#             highest_rated = clothing_data.loc[clothing_data['Rating'].idxmax()]
#             st.write(knowledge_base[best_match_key].format(
#                 type=highest_rated['Type'],
#                 brand=highest_rated['Brand'],
#                 rating=highest_rated['Rating']
#             ))

#         elif best_match_key == "discounts":
#             discounts = clothing_data[clothing_data['Discount'] != '0%']
#             st.write(knowledge_base[best_match_key].format(num_discounts=len(discounts)))



import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load semantic search model
model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

# Predefined data
types = ['Shirt', 'T-shirt', 'Jeans', 'Jacket', 'Dress', 'Shorts', 'Sweater', 'Skirt', 'Blouse', 'Hoodie']
brands = ['Zara', 'Nike', 'Biba', 'Adidas', 'H&M', 'Levi\'s', 'Forever 21', 'Raymond', 'FabIndia', 'Puma']
colors = ['Blue', 'Black', 'Blue', 'Grey', 'Red', 'Black', 'Pink', 'Blue', 'Green', 'Red']
prices = [1299, 1199, 2499, 3299, 2999, 1499, 1999, 1699, 1799, 2499]
discounts = ['10%', '5%', '20%', '15%', '0%', '10%', '25%', '5%', '10%', '20%']
ratings = [4.2, 4.5, 4.0, 4.8, 4.3, 3.9, 4.6, 4.1, 4.2, 4.4]
delivery_times = ['2 days', '3 days', '4 days', '1 day', '5 days', '3 days', '2 days', '3 days', '4 days', '1 day']
shapes = ['Slim Fit', 'Regular', 'Straight', 'Regular', 'A-line', 'Slim Fit', 'Regular', 'Flared', 'Regular', 'Regular']
occasions = ['Casual', 'Sports', 'Casual', 'Winter', 'Formal', 'Casual', 'Winter', 'Casual', 'Formal', 'Sports']
sizes = ['M', 'S', 'L', 'L', 'M', 'M', 'L', 'S', 'M', 'XL']

# Combine into a DataFrame
clothing_data = pd.DataFrame({
    'Type': types,
    'Brand': brands,
    'Color': colors,
    'Price': prices,
    'Discount': discounts,
    'Rating': ratings,
    'Delivery Time': delivery_times,
    'Shape': shapes,
    'Occasion': occasions,
    'Size': sizes
})

# Streamlit interface
st.title("Clothing Store Bot")

# Knowledge base for queries
knowledge_base = {
    "brands": "We have {num_brands} unique brands available, those are : <br>{brands}",
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

# Encode queries for semantic matching
encoded_knowledge = model.encode(list(knowledge_base.keys()), convert_to_tensor=True)

# User query input
user_query = st.text_input("Ask me anything about our clothing store:")

SIMILARITY_THRESHOLD = 0.7  # Adjusted for stricter filtering

if user_query:
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    # Normalize embeddings
    query_embedding = query_embedding / query_embedding.norm(dim=0)  # For 1D tensor
    encoded_knowledge = encoded_knowledge / encoded_knowledge.norm(dim=1, keepdim=True)  # For 2D tensor

    
    dot_products = util.dot_score(query_embedding, encoded_knowledge)[0]
    best_match_idx = dot_products.argmax().item()
    best_match_score = dot_products[best_match_idx].item()
    best_match_key = list(knowledge_base.keys())[best_match_idx]

    if best_match_score < SIMILARITY_THRESHOLD:
        st.write("Sorry...!! I can only answer questions about clothing.")
    else:
        if best_match_key == "brands":
            num_brands = clothing_data['Brand'].nunique()
            brandS = ', '.join(clothing_data['Brand'].unique())  # Join brands with commas
            st.markdown(knowledge_base[best_match_key].format(num_brands=num_brands, brands=brandS), unsafe_allow_html=True)
        elif best_match_key == "types":
            unique_types = ', '.join(clothing_data['Type'].unique())
            st.write(knowledge_base[best_match_key].format(types=unique_types))

        elif best_match_key == "average price":
            avg_price = clothing_data['Price'].mean()
            st.write(knowledge_base[best_match_key].format(avg_price=avg_price))

        elif best_match_key == "highest rated":
            highest_rated = clothing_data.loc[clothing_data['Rating'].idxmax()]
            st.write(knowledge_base[best_match_key].format(
                type=highest_rated['Type'],
                brand=highest_rated['Brand'],
                rating=highest_rated['Rating']
            ))

        elif best_match_key == "discounts":
            discounts = clothing_data[clothing_data['Discount'] != '0%']
            st.write(knowledge_base[best_match_key].format(num_discounts=len(discounts)))

        elif best_match_key == "colors":
            unique_colors = ', '.join(clothing_data['Color'].unique())
            st.write(knowledge_base[best_match_key].format(colors=unique_colors))

        elif best_match_key == "sizes":
            unique_sizes = ', '.join(clothing_data['Size'].unique())
            st.write(knowledge_base[best_match_key].format(sizes=unique_sizes))

        elif best_match_key == "fastest delivery":
            fastest_delivery = clothing_data.loc[clothing_data['Delivery Time'].idxmin()]
            st.write(knowledge_base[best_match_key].format(
                delivery_time=fastest_delivery['Delivery Time'],
                type=fastest_delivery['Type'],
                brand=fastest_delivery['Brand']
            ))

        elif best_match_key == "best deal":
            best_deal = clothing_data.loc[clothing_data['Discount'].str.rstrip('%').astype(int).idxmax()]
            st.write(knowledge_base[best_match_key].format(
                discount=best_deal['Discount'],
                type=best_deal['Type'],
                brand=best_deal['Brand']
            ))

        elif best_match_key == "price range":
            min_price = clothing_data['Price'].min()
            max_price = clothing_data['Price'].max()
            st.write(knowledge_base[best_match_key].format(min_price=min_price, max_price=max_price))

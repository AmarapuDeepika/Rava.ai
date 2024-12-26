import streamlit as st
import pandas as pd
import random
from sentence_transformers import SentenceTransformer, util

# Load semantic search model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to generate random clothing data
def generate_clothing_data(num_items):
    types = ['Shirt', 'T-shirt', 'Jeans', 'Jacket', 'Dress', 'Shorts', 'Sweater', 'Skirt', 'Blouse', 'Hoodie']
    brands = ['Levi\'s', 'Nike', 'Wrangler', 'Adidas', 'Zara', 'H&M', 'Uniqlo', 'Mango', 'Ralph Lauren', 'Puma']
    colors = ['Blue', 'Red', 'Black', 'Grey', 'Green', 'White', 'Navy', 'Pink']
    shapes = ['Slim Fit', 'Regular', 'Straight', 'A-line', 'V-neck', 'Flared']
    occasions = ['Casual', 'Sports', 'Winter', 'Formal']
    sizes = ['S', 'M', 'L', 'XL', '32']

    data = []
    for i in range(num_items):
        item_id = i + 1
        type_ = random.choice(types)
        brand = random.choice(brands)
        color = random.choice(colors)
        price = round(random.uniform(20, 100), 2)
        discount = random.choice([0, 5, 10, 15, 20, 25, 30])
        rating = round(random.uniform(3, 5), 1)
        delivery_time = random.choice([1, 2, 3, 4, 5])  # Days
        shape = random.choice(shapes)
        occasion = random.choice(occasions)
        size = random.choice(sizes)

        item = {
            'Item ID': item_id,
            'Type': type_,
            'Brand': brand,
            'Color': color,
            'Price': price,
            'Discount': f"{discount}%",
            'Rating': rating,
            'Delivery Time': f"{delivery_time} days",
            'Shape': shape,
            'Occasion': occasion,
            'Size': size
        }

        data.append(item)

    return pd.DataFrame(data)

# Generate the clothing dataset
clothing_data = generate_clothing_data(100)

# Streamlit interface
st.title("Clothing Store Bot")

# Knowledge base for queries
knowledge_base = {
    "brands": "We have {num_brands} unique brands available.",
    "types": "We offer the following types of clothing: {types}.",
    "average price": "The average price of our clothing is ${avg_price:.2f}.",
    "highest rated": "The highest-rated item is a {type} from {brand} with a rating of {rating}.",
    "discounts": "{num_discounts} items currently have discounts.",
    "colors": "We offer clothing in the following colors: {colors}.",
    "sizes": "Available sizes are: {sizes}.",
    "fastest delivery": "The fastest delivery time is {delivery_time} for {type} from {brand}.",
    "best deal": "The highest discount is {discount} on {type} from {brand}.",
    "price range": "Our prices range from ${min_price:.2f} to ${max_price:.2f}."
}

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

    if best_match_key == "brands":
        num_brands = clothing_data['Brand'].nunique()
        st.write(knowledge_base[best_match_key].format(num_brands=num_brands))

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
    else:
        #st.write(knowledge_base[best_match_key])
        st.write("Sorry, I don't have that information")


import streamlit as st
import pandas as pd
import random
import re

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

# User query input
user_query = st.text_input("Ask me anything about our clothing store:")

# Process query and respond
if user_query:
    user_query = user_query.lower()

    if re.search(r'how many brands', user_query):
        num_brands = clothing_data['Brand'].nunique()
        st.write(f"We have {num_brands} unique brands available.")

    elif re.search(r'how many types|what types of dresses', user_query):
        unique_types = clothing_data['Type'].unique()
        st.write(f"We offer the following types of clothing: {', '.join(unique_types)}.")

    elif re.search(r'average price', user_query):
        avg_price = clothing_data['Price'].mean()
        st.write(f"The average price of our clothing is ${avg_price:.2f}.")

    elif re.search(r'highest rated', user_query):
        highest_rated = clothing_data.loc[clothing_data['Rating'].idxmax()]
        st.write(f"The highest-rated item is a {highest_rated['Type']} from {highest_rated['Brand']} with a rating of {highest_rated['Rating']}.")

    elif re.search(r'discount|on sale', user_query):
        discounts = clothing_data[clothing_data['Discount'] != '0%']
        st.write(f"{len(discounts)} items currently have discounts.")

    elif re.search(r'what colors|available colors', user_query):
        unique_colors = clothing_data['Color'].unique()
        st.write(f"We offer clothing in the following colors: {', '.join(unique_colors)}.")

    elif re.search(r'what sizes|available sizes', user_query):
        unique_sizes = clothing_data['Size'].unique()
        st.write(f"Available sizes are: {', '.join(unique_sizes)}.")

    elif re.search(r'fastest delivery', user_query):
        fastest_delivery = clothing_data.loc[clothing_data['Delivery Time'].idxmin()]
        st.write(f"The fastest delivery time is {fastest_delivery['Delivery Time']} for {fastest_delivery['Type']} from {fastest_delivery['Brand']}.")

    elif re.search(r'best deal|highest discount', user_query):
        best_deal = clothing_data.loc[clothing_data['Discount'].str.rstrip('%').astype(int).idxmax()]
        st.write(f"The highest discount is {best_deal['Discount']} on {best_deal['Type']} from {best_deal['Brand']}.")

    elif re.search(r'clothes for casual|sports|winter|formal', user_query):
        match = re.search(r'casual|sports|winter|formal', user_query)
        occasion = match.group()
        occasion_clothes = clothing_data[clothing_data['Occasion'].str.contains(occasion, case=False)]
        st.write(f"We have {len(occasion_clothes)} items suitable for {occasion} occasions.")

    elif re.search(r'price range', user_query):
        min_price = clothing_data['Price'].min()
        max_price = clothing_data['Price'].max()
        st.write(f"Our prices range from ${min_price:.2f} to ${max_price:.2f}.")

    elif re.search(r'latest arrivals|new items', user_query):
        latest_items = clothing_data.tail(5)
        st.write("Here are the 5 latest items in our collection:")
        st.dataframe(latest_items)

    else:
        st.write("I'm sorry, I couldn't understand your query. Please ask about brands, types, prices, ratings, colors, sizes, discounts, occasions, or delivery times.")

# Show full dataset if requested
if st.checkbox("Show full dataset"):
    st.dataframe(clothing_data)

import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_excel('large_festival_sales_data.xlsx')

# Preprocess the data
label_encoder_category = LabelEncoder()
label_encoder_product = LabelEncoder()
label_encoder_festival = LabelEncoder()
label_encoder_gender = LabelEncoder()
label_encoder_month = LabelEncoder()

df['Category'] = label_encoder_category.fit_transform(df['Category'])
df['Product'] = label_encoder_product.fit_transform(df['Product'])
df['Festival'] = label_encoder_festival.fit_transform(df['Festival'])
df['Gender'] = label_encoder_gender.fit_transform(df['Gender'])
df['Month'] = label_encoder_month.fit_transform(df['Month'])

# Streamlit UI
st.title("Festival Sales Prediction")

# Dropdown inputs
festival = st.selectbox("Select Festival", label_encoder_festival.classes_)
year = st.selectbox("Select Year", df['Year'].unique())
gender = st.selectbox("Select Gender", label_encoder_gender.classes_)
category = st.selectbox("Select Category", label_encoder_category.classes_)

# Predict the best-selling product for the selected festival, year, gender, and category
if st.button('Get Best-Selling Products'):

    # Filter data based on selected festival, year, gender, and category
    selected_festival = label_encoder_festival.transform([festival])[0]
    selected_gender = label_encoder_gender.transform([gender])[0]
    selected_category = label_encoder_category.transform([category])[0]
    
    filtered_df = df[(df['Festival'] == selected_festival) & 
                     (df['Year'] == year) & 
                     (df['Gender'] == selected_gender) & 
                     (df['Category'] == selected_category)]

    if not filtered_df.empty:
        # Sort the products by sales to get the top sellers
        top_selling_products = filtered_df.sort_values(by='Sales', ascending=False)

        # Decode the product names
        top_selling_products['Product'] = label_encoder_product.inverse_transform(top_selling_products['Product'])
        
        # Display the top products along with their sales numbers
        st.write(f"Top-selling products for {festival} in {year} (Gender: {gender}, Category: {category}):")
        for index, row in top_selling_products.iterrows():
            st.write(f"{row['Product']} - Sold {row['Sales']} units")
    else:
        st.write("No sales data available for the selected festival, year, gender, and category.")




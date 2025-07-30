import streamlit as st
import pandas as pd

# Load the dataset from the CSV file
merged_df = pd.read_csv('df_merged.csv')  # Ensure this file is in the same directory or provide the full path

# Function for item-based recommendation
def item_based_recommender(product_name, data):
    product_data = data.pivot_table(index='UserID', columns='Nama', values='Rating')  # Adjust column names if necessary
    
    if product_name not in product_data.columns:
        st.error(f"Product '{product_name}' not found.")
        return None
    
    # Calculate similarity
    product_ratings = product_data[product_name]
    similar_products = product_data.corrwith(product_ratings).sort_values(ascending=False).head(10)
    return similar_products

# Streamlit App
st.title("Sistem Rekomendasi Produk Kecantikan")

# User input for User ID at the top
user_id = st.number_input("Masukkan ID Pengguna", min_value=1, step=1)

# User input for selecting a product
product_name = st.selectbox("Pilih Produk", merged_df['Nama'].unique())  # Adjust if needed

# User input for selecting a jenis kulit
skin_type = st.selectbox("Pilih Jenis Kulit", merged_df['Tipe Kulit'].unique())  # Adjust if needed

# Option to get recommendations
if st.button('Rekomendasikan'):
    recommendations = item_based_recommender(product_name, merged_df)
    
    if recommendations is not None:
        # Convert recommendations to a DataFrame
        recommendations_df = recommendations.reset_index()
        recommendations_df.columns = ['Product', 'Similarity']  # Rename columns for clarity
        
        st.write("Top 10 recommended products:")
        st.dataframe(recommendations_df)  # Display recommendations in a table format

# Get the user’s past ratings for products (if available)
user_data = merged_df[merged_df['UserID'] == user_id]
if not user_data.empty:
    st.write("Your past ratings:")
    st.dataframe(user_data[['Nama', 'Rating']])  # Adjust if needed
else:
    st.write("No previous ratings found for this User ID.")

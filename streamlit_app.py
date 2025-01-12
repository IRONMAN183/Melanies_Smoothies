# Import python packages
import pandas as pd  # Shortened to pd for easier use
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

# Input for the name of the order
name_on_order = st.text_input('Name on Order', placeholder="Enter your name here")
st.write('The name on the smoothie will be:', name_on_order)

# Get Snowflake session and retrieve available fruit options
cnx = st.connection("snowflake")
session = cnx.session()

# Query Snowflake and convert to Pandas DataFrame
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()  # Convert Snowflake DataFrame to Pandas
st.dataframe(pd_df)  # Display the Pandas DataFrame for debugging

# Extract fruit names as a list
fruit_list = pd_df['FRUIT_NAME'].tolist()

# Multi-select for ingredients with a maximum of 5 selections
ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients:', 
    fruit_list, 
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        # Get the corresponding SEARCH_ON value for the selected fruit
        if fruit_chosen in pd_df['FRUIT_NAME'].values:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
            
            # Fetch and display nutrition information
            st.subheader(f"{fruit_chosen} Nutrition Information")
            smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/all/ " + {search_on})
            if smoothiefroot_response.status_code == 200:
                st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            else:
                st.error(f"Failed to fetch data for {fruit_chosen}.")
        else:
            st.error(f"Fruit '{fruit_chosen}' not found in the database.")
#https://my.smoothiefroot.com/api/fruit/
# Button to submit order
time_to_insert = st.button('Submit Order')

if time_to_insert:
    if name_on_order and ingredients_list:
        # Construct the SQL statement with formatted placeholders
        ingredients_string = ', '.join(ingredients_list)  # Join ingredients into a single string
        insert_query = f"""
            INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        try:
            # Execute the SQL query
            session.sql(insert_query).collect()
            st.success(f'Your Smoothie Ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error('Please enter a name and select ingredients!', icon="❌")

# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd  # Added pandas with alias pd

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
fruit_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=fruit_dataframe, use_container_width=True)
# st.stop() -- Uncomment this for debugging if needed
fruit_list = [row['FRUIT_NAME'] for row in fruit_dataframe.collect()]  # Convert to a Python list

# Convert Snowflake data to Pandas DataFrame
fruit_pandas_df = pd.DataFrame(fruit_dataframe.collect())  # Now you can work with the data in Pandas
st.write(fruit_pandas_df)  # Display the Pandas DataFrame for debugging (optional)

# Multi-select for ingredients with a maximum of 5 selections
ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients:', 
    fruit_list, 
    max_selections=5
)

if ingredients_list:
    for fruit_chosen in ingredients_list:
        search_on_value = fruit_dataframe.filter(col('FRUIT_NAME') == fruit_chosen).collect()[0]['SEARCH_ON']
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on_value)
        if smoothiefroot_response.status_code == 200:
            st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        else:
            st.error(f"Could not retrieve data for {fruit_chosen}.")

# Submit button logic
if st.button('Submit Order'):
    if name_on_order and ingredients_list:
        ingredients_string = ' '.join(ingredients_list)
        try:
            session.sql("""
                INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
                VALUES (:ingredients, :name)
            """).bind("ingredients", ingredients_string).bind("name", name_on_order).collect()
            st.success(f'Your Smoothie Ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error('Please enter a name and select ingredients!', icon="❌")

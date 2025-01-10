# Import python packages
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
fruit_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = [row['FRUIT_NAME'] for row in fruit_dataframe.collect()]  # Convert to a Python list

# Multi-select for ingredients with a maximum of 5 selections
ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients:', 
    fruit_list, 
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
#updated 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    # Add your parameters here for selecting fruits
)

#if ingredients_list:
 #   ingredients_string = ''

  #  for fruit_chosen in ingredients_list:
   #     ingredients_string += fruit_chosen + ' '
   #     smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    #    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


# Display selected ingredients
#if ingredients_list:
    #ingredients_string = ', '.join(ingredients_list)  # Create a comma-separated string
    #st.write('You selected:', ingredients_string)
#else:
    #ingredients_string = None

# Button to submit order
time_to_insert = st.button('Submit Order')

if time_to_insert:
    if name_on_order and ingredients_string:
        # Construct the SQL statement with placeholders
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        try:
            # Execute the SQL query
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie Ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error('Please enter a name and select ingredients!', icon="❌")





smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


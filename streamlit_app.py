# Streamlit setup code

# Display dataframe
st.dataframe(data=fruit_dataframe, use_container_width=True)

# Select up to 5 ingredients
ingredients_list = st.multiselect('Choose up to 5 Ingredients:', fruit_list, max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    for fruit_chosen in ingredients_list:
        search_on_value = fruit_dataframe.filter(col('FRUIT_NAME') == fruit_chosen).collect()[0]['SEARCH_ON']
        st.subheader(fruit_chosen + ' Nutrition Information')
        with st.spinner('Fetching nutrition data...'):
            smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on_value}")
            if smoothiefroot_response.status_code == 200:
                st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            else:
                st.error(f"Could not retrieve data for {fruit_chosen}.")

# Submit button logic
if time_to_insert:
    if name_on_order and ingredients_list:
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
